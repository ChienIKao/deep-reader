#!/usr/bin/env python3
"""Assemble one tabbed deep-reader HTML page from per-mode body fragments.

Usage:
    python build_page.py --title "Paper Title" --subtitle "Author · Year" \
        --summary summary.html \
        --translate tr-01.html tr-02.html \
        --annotate annotate.html \
        --logic logic.html \
        --out paper-reader.html

Give only the modes you produced; each becomes one tab, in the order
Key Points → Translation → Annotated → Logic Map. A mode's fragments are
concatenated in the order given, so long translations can be written in parts.

The template is ../assets/reader.html with two placeholders: {{TITLE}}
(plain text, HTML-escaped) and {{BODY}} (the app bar, panels and footer this
script generates). Paragraph anchors are namespaced per tab (tr-pN / an-pN);
plain id="pN" / href="#pN" in a fragment are rewritten automatically.
Only the Python standard library is used.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
TEMPLATE = ASSETS / "reader.html"
# (cli option, panel id, tab label, paragraph-anchor prefix)
MODES = (
    ("summary", "tab-summary", "Key Points", None),
    ("translate", "tab-translate", "Translation", "tr-"),
    ("annotate", "tab-annotate", "Annotated", "an-"),
    ("logic", "tab-logic", "Logic Map", None),
)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
CHECKED = {"section", "div", "article", "main", "header", "footer", "ul", "ol", "li", "table", "tr", "details", "dl", "p", "mark", "blockquote", "nav"}


class BalanceChecker(HTMLParser):
    """Report unclosed or stray structural tags — the usual cause of a broken layout."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.problems: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in CHECKED and tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag not in CHECKED:
            return
        if not any(t == tag for t, _ in self.stack):
            self.problems.append(f"line {self.getpos()[0]}: stray </{tag}>")
            return
        while self.stack:
            t, line = self.stack.pop()
            if t == tag:
                break
            # <p> and <li> may be implicitly closed; everything else is a real problem
            if t not in ("p", "li"):
                self.problems.append(f"line {line}: <{t}> not closed before </{tag}>")

    def finish(self) -> list[str]:
        for t, line in self.stack:
            if t not in ("p", "li"):
                self.problems.append(f"line {line}: <{t}> never closed")
        return self.problems


def namespace_anchors(body: str, prefix: str) -> str:
    """Rewrite bare paragraph anchors (pN) so two tabs never share an id."""
    body = re.sub(r'\bid="p(\d+)"', rf'id="{prefix}p\1"', body)
    return re.sub(r'href="#p(\d+)"', rf'href="#{prefix}p\1"', body)


def summarize(mode: str, body: str) -> str:
    if mode == "summary":
        blocks = len(re.findall(r'class="kp"', body))
        return f"Key Points: {blocks} sections"
    if mode == "translate":
        pairs = len(re.findall(r'class="pair(?:\s[^"]*)?"', body))
        numbered = len(re.findall(r'<section[^>]*\bid="tr-p\d+"', body))
        return f"Translation: {pairs} pair rows ({numbered} numbered paragraphs)"
    if mode == "annotate":
        pairs = len(re.findall(r'class="pair(?:\s[^"]*)?"', body))
        qs = sorted(set(re.findall(r'class="chip (q\d)"', body)))
        marks = len(re.findall(r"<mark\b", body))
        answers = len(re.findall(r'class="answer q\d', body))
        msg = f"Annotated: {pairs} pair rows; legend {', '.join(qs) or 'none'}; {marks} highlights; {answers} answer cards"
        missing = set(re.findall(r'<mark class="(q\d)"', body)) - set(qs)
        if missing:
            msg += f"; WARNING: marks use {sorted(missing)} but the legend lacks them"
        return msg
    nodes = len(re.findall(r'class="node ', body))
    steps = len(re.findall(r'class="step"', body))
    return f"Logic Map: {nodes} argument-map nodes; {steps} flow steps"


def read_fragments(paths: list[str]) -> str | None:
    chunks = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            print(f"error: body fragment not found: {path}", file=sys.stderr)
            return None
        chunks.append(path.read_text(encoding="utf-8").strip())
    return "\n\n".join(chunks)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title", required=True, help="document title (plain text)")
    ap.add_argument("--subtitle", default="", help="author / year / course, shown next to the title")
    for opt, _, label, _ in MODES:
        ap.add_argument(f"--{opt}", nargs="+", metavar="FRAGMENT", help=f"fragment file(s) for the {label} tab")
    ap.add_argument("--out", required=True, help="output .html path")
    args = ap.parse_args()

    if not TEMPLATE.exists():
        print(f"error: template not found: {TEMPLATE}", file=sys.stderr)
        return 2

    tabs, panels, report, problems = [], [], [], []
    for opt, pid, label, prefix in MODES:
        files = getattr(args, opt)
        if not files:
            continue
        body = read_fragments(files)
        if body is None:
            return 2
        if prefix:
            body = namespace_anchors(body, prefix)
        leftover = re.findall(r"\{\{[A-Z_]+\}\}", body)
        if leftover:
            print(f"warning: {label}: unfilled placeholders {sorted(set(leftover))}", file=sys.stderr)
        checker = BalanceChecker()
        checker.feed(body)
        problems += [f"{label}: {m}" for m in checker.finish()]
        tabs.append(f'<button type="button" role="tab" data-tab="{pid}" aria-controls="{pid}">{label}</button>')
        panels.append(f'<section class="panel" id="{pid}" role="tabpanel" aria-label="{label}">\n{body}\n</section>')
        report.append(summarize(opt, body))

    if not panels:
        print("error: give at least one of --summary / --translate / --annotate / --logic", file=sys.stderr)
        return 2
    for msg in problems[:20]:
        print(f"warning: {msg}", file=sys.stderr)
    if len(problems) > 20:
        print(f"warning: ... and {len(problems) - 20} more", file=sys.stderr)

    title = html.escape(args.title, quote=False)
    sub = f"<small>{html.escape(args.subtitle, quote=False)}</small>" if args.subtitle else ""
    header = (
        '<header class="appbar">\n  <div class="appbar-inner">\n'
        f'    <div class="app-title">{title}{sub}</div>\n'
        '    <nav class="tabs" role="tablist" aria-label="Views">\n      '
        + "\n      ".join(tabs)
        + "\n    </nav>\n  </div>\n</header>"
    )
    foot = '<footer class="app-foot">Generated by deep-reader · A study aid — check it against the original text</footer>'
    body = "\n\n".join([header, *panels, foot])

    page = TEMPLATE.read_text(encoding="utf-8").replace("{{TITLE}}", title).replace("{{BODY}}", body)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out} ({len(page):,} chars) - {len(panels)} tab(s)")
    for line in report:
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
