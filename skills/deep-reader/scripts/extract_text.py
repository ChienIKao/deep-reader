#!/usr/bin/env python3
"""Extract clean, paragraph-separated text from a PDF, a web page, or a text file.

Usage:
    python extract_text.py paper.pdf -o paper.txt
    python extract_text.py https://example.com/article -o article.txt
    python extract_text.py paper.pdf --pages 1-12

Output: paragraphs separated by blank lines. PDF page boundaries are marked
with lines like "[[page 3]]" so paragraphs can be traced back to the source.

PDF backends, tried in order: PyMuPDF (fitz), pypdf, pdfminer.six.
Install one if none is available:  pip install pymupdf
Web pages use only the standard library.
"""
from __future__ import annotations

import argparse
import io
import re
import sys
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


# ---------------------------------------------------------------- PDF

def pdf_pages(data: bytes) -> list[str]:
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(stream=data, filetype="pdf")
        pages = []
        for page in doc:
            # sort=True yields natural reading order, which matters for two-column papers
            blocks = page.get_text("blocks", sort=True)
            pages.append("\n\n".join(b[4].strip() for b in blocks if b[6] == 0 and b[4].strip()))
        return pages
    except ImportError:
        pass
    try:
        from pypdf import PdfReader

        return [(p.extract_text() or "") for p in PdfReader(io.BytesIO(data)).pages]
    except ImportError:
        pass
    try:
        from pdfminer.high_level import extract_text

        return extract_text(io.BytesIO(data)).split("\f")
    except ImportError:
        pass
    sys.exit("error: no PDF library found. Install one with:  pip install pymupdf   (or: pip install pypdf)")


def strip_repeating_lines(pages: list[str]) -> list[str]:
    """Remove running headers/footers: short lines that recur on many pages."""
    if len(pages) < 3:
        return pages
    norm = lambda s: re.sub(r"\d+", "#", s.strip().lower())
    counts = Counter()
    for p in pages:
        lines = [l for l in p.splitlines() if l.strip()]
        edge = lines[:3] + lines[-3:]
        counts.update({norm(l) for l in edge if len(l.strip()) < 120})
    threshold = max(3, int(len(pages) * 0.4))
    noisy = {k for k, v in counts.items() if v >= threshold}
    out = []
    for p in pages:
        kept = [l for l in p.splitlines() if norm(l) not in noisy]
        out.append("\n".join(kept))
    return out


PAGE_NUM = re.compile(r"^\s*(page\s*)?\d{1,4}(\s*(of|/)\s*\d{1,4})?\s*$", re.I)
NOISE = re.compile(r"^(downloaded from|this content downloaded|all use subject to|©|copyright \d{4})", re.I)


def reflow(text: str) -> list[str]:
    """Join hard-wrapped lines into paragraphs and repair end-of-line hyphenation."""
    paras: list[str] = []
    for block in re.split(r"\n\s*\n", text):
        lines = [l.strip() for l in block.splitlines()]
        lines = [l for l in lines if l and not PAGE_NUM.match(l) and not NOISE.match(l)]
        if not lines:
            continue
        buf = lines[0]
        for line in lines[1:]:
            if re.search(r"[A-Za-z]-$", buf) and line[:1].islower():
                buf = buf[:-1] + line  # exam- / ple -> example
            else:
                buf += " " + line
        paras.append(re.sub(r"\s{2,}", " ", buf).strip())
    return paras


SENTENCE_END = re.compile(r"[.!?…][\"'”’)\]]*$")
CAPTION = re.compile(r"^(fig\.?|figure|table|tab\.|algorithm|listing|chart|plate)\s*[\dIVX]", re.I)
FOOTNOTE = re.compile(r"^([∗*†‡§]|\d{1,2}(?=[A-Za-z]))")
HEADING = re.compile(r"^(\d+(\.\d+)*\.?|[IVX]+\.|[A-Z]\.)\s+[A-Z]")
REFS = re.compile(r"^(\d+\.?\s+)?(references|bibliography|works cited|literature cited)\s*$", re.I)
LIST_ITEM = re.compile(r"^(\[\d+\]|\(?\d{1,3}[.)]\s|[•▪◦–-]\s)")
FUNCTION_WORDS = {
    "a", "an", "the", "of", "to", "in", "on", "at", "by", "for", "with", "from", "as", "into", "than",
    "and", "or", "but", "nor", "that", "which", "who", "whom", "whose", "is", "are", "was", "were",
    "be", "been", "this", "these", "those", "its", "their", "his", "her", "our", "we", "it", "not",
    "if", "when", "while", "because", "such", "between", "about", "under", "over", "via",
}
# a page that ends on one of these words cannot be the end of a sentence
DANGLING = FUNCTION_WORDS - {"it", "we", "this", "these", "those", "not"}


def is_prose(p: str) -> bool:
    """Running English text has function words; tables, formulas and author lists mostly don't."""
    chars = re.sub(r"\s", "", p)
    if sum(c.isdigit() for c in chars) / max(1, len(chars)) >= 0.15:
        return False  # table rows, numeric results
    words = re.findall(r"[A-Za-z’']+", p)
    if len(words) < 8:
        return p[:1].islower()
    return sum(w.lower() in FUNCTION_WORDS for w in words) / len(words) >= 0.12


def join_fragments(head: str, tail: str) -> str:
    if re.search(r"[A-Za-z]-$", head) and tail[:1].islower():
        return head[:-1] + tail  # exam- / ple -> example
    return head + " " + tail


def stitch_pages(pages: list[list[str]]) -> int:
    """Re-join paragraphs that a page break cut in half (in place).

    A page often ends mid-sentence, and the rest of that sentence is printed on the
    next page after running headers, figure labels or captions. Left alone, the second
    half looks like an orphan fragment and tends to get dropped or mistranslated.
    Returns the number of paragraphs stitched.
    """
    stitched = 0
    for n in range(len(pages) - 1):
        cur, nxt = pages[n], pages[n + 1]
        if any(REFS.match(p) for p in cur):
            break  # reference lists are kept verbatim and never translated; don't risk gluing entries

        # last body paragraph on this page, skipping trailing footnotes / short footer lines
        idx = next((j for j in range(len(cur) - 1, -1, -1)
                    if len(cur[j]) >= 60 and not CAPTION.match(cur[j]) and not FOOTNOTE.match(cur[j])), None)
        if idx is None or SENTENCE_END.search(cur[idx]):
            continue
        head = cur[idx]
        last_word = (re.findall(r"[A-Za-z]+", head[-30:]) or [""])[-1].lower()
        # walk past figure labels, captions and tables at the top of the next page
        k = None
        for j, p in enumerate(nxt[:10]):
            if HEADING.match(p) and len(p) < 120:
                break  # a new section starts: the cut paragraph really ended on the previous page
            if CAPTION.match(p) or LIST_ITEM.match(p) or not is_prose(p):
                continue
            if len(p) < 60 and not p[:1].islower():
                continue  # short label such as a figure's internal text
            # lowercase start is a safe continuation; otherwise demand a dangling last word
            if p[:1].islower() or (last_word in DANGLING or head.endswith((",", "-", "—"))):
                k = j
            break  # never skip over a real prose paragraph
        if k is None:
            continue
        cont = nxt[k]
        cur[idx] = join_fragments(head, cont)
        del nxt[k]
        stitched += 1
    return stitched


def from_pdf(data: bytes, page_range: tuple[int, int] | None) -> str:
    pages = pdf_pages(data)
    if page_range:
        lo, hi = page_range
        pages = pages[lo - 1 : hi]
        offset = lo
    else:
        offset = 1
    pages = strip_repeating_lines(pages)
    page_paras = [reflow(page) for page in pages]
    stitched = stitch_pages(page_paras)
    if stitched:
        print(f"note: re-joined {stitched} paragraph(s) split across page breaks", file=sys.stderr)
    out = []
    total_chars = 0
    for i, paras in enumerate(page_paras, start=offset):
        total_chars += sum(len(p) for p in paras)
        out.append(f"[[page {i}]]")
        out.extend(paras)
    if pages and total_chars / len(pages) < 200:
        print(
            f"warning: only ~{total_chars // max(1, len(pages))} characters per page were extracted. "
            "The PDF is probably scanned images; ask the user for a text version or use OCR.",
            file=sys.stderr,
        )
    return "\n\n".join(out)


# ---------------------------------------------------------------- HTML

class ArticleParser(HTMLParser):
    BLOCK = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "blockquote", "pre", "figcaption", "td", "th", "dt", "dd"}
    SKIP = {"script", "style", "noscript", "nav", "header", "footer", "aside", "form", "svg", "button", "iframe"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.in_article = 0
        self.saw_article = False
        self.cur: list[str] | None = None
        self.cur_tag = ""
        self.blocks: list[tuple[str, str, bool]] = []  # (tag, text, inside <article>/<main>)
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag in ("article", "main"):
            self.in_article += 1
            self.saw_article = True
        elif tag == "title":
            self._in_title = True
        elif tag in self.BLOCK and not self.skip:
            self._flush()
            self.cur, self.cur_tag = [], tag
        elif tag == "br" and self.cur is not None:
            self.cur.append(" ")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
        elif tag in ("article", "main"):
            self.in_article = max(0, self.in_article - 1)
        elif tag == "title":
            self._in_title = False
        elif tag in self.BLOCK:
            self._flush()

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif self.cur is not None and not self.skip:
            self.cur.append(data)

    def _flush(self):
        if self.cur is not None:
            text = re.sub(r"\s+", " ", "".join(self.cur)).strip()
            if text:
                self.blocks.append((self.cur_tag, text, self.in_article > 0))
        self.cur = None


def from_html(raw: str) -> str:
    p = ArticleParser()
    p.feed(raw)
    p._flush()
    blocks = [b for b in p.blocks if b[2]] if p.saw_article else p.blocks
    # drop short boilerplate (menus, share buttons) but keep headings
    blocks = [b for b in blocks if b[0].startswith("h") or len(b[1]) > 40 or b[0] in ("li", "blockquote")]
    out = []
    if p.title.strip():
        out.append(f"# {p.title.strip()}")
    for tag, text, _ in blocks:
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            out.append("#" * int(tag[1]) + " " + text)
        elif tag == "li":
            out.append("- " + text)
        elif tag == "blockquote":
            out.append("> " + text)
        else:
            out.append(text)
    return "\n\n".join(out)


# ---------------------------------------------------------------- main

def fetch(url: str) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/pdf,*/*"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read(), resp.headers.get("Content-Type", "")


def parse_range(s: str | None) -> tuple[int, int] | None:
    if not s:
        return None
    m = re.fullmatch(r"(\d+)(?:-(\d+))?", s.strip())
    if not m:
        sys.exit("error: --pages must look like 3 or 1-12")
    lo = int(m.group(1))
    return lo, int(m.group(2) or lo)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="PDF/text file path or http(s) URL")
    ap.add_argument("-o", "--out", help="write to this file instead of stdout")
    ap.add_argument("--pages", help="PDF page range, e.g. 1-12")
    args = ap.parse_args()

    src = args.source
    if re.match(r"https?://", src):
        try:
            data, ctype = fetch(src)
        except Exception as e:  # network errors, 403 paywalls, etc.
            sys.exit(f"error: could not fetch {src}: {e}. Ask the user to paste the text instead.")
        if "pdf" in ctype.lower() or data[:5] == b"%PDF-":
            text = from_pdf(data, parse_range(args.pages))
        else:
            charset = (re.search(r"charset=([\w-]+)", ctype) or [None, "utf-8"])[1]
            text = from_html(data.decode(charset, errors="replace"))
    else:
        path = Path(src)
        if not path.exists():
            sys.exit(f"error: file not found: {path}")
        data = path.read_bytes()
        if path.suffix.lower() == ".pdf" or data[:5] == b"%PDF-":
            text = from_pdf(data, parse_range(args.pages))
        elif path.suffix.lower() in (".html", ".htm"):
            text = from_html(data.decode("utf-8", errors="replace"))
        else:
            text = data.decode("utf-8", errors="replace")

    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        words = len(re.findall(r"[A-Za-z]+", text))
        paras = len([p for p in text.split("\n\n") if p.strip() and not p.startswith("[[page")])
        print(f"wrote {args.out}: ~{words:,} English words, {paras} paragraphs")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
