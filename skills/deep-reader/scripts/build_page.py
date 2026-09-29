#!/usr/bin/env python3
"""Assemble a deep-reader HTML page from a template and one or more body fragments.

Usage:
    python build_page.py --template translate --title "Paper Title" \
        --body part-01.html part-02.html --out paper-translate.html

Templates live in ../assets/<template>.html and contain two placeholders:
{{TITLE}} (plain text, will be HTML-escaped) and {{BODY}} (raw HTML).
Fragments are concatenated in the order given. Only the Python standard
library is used.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
TEMPLATES = ("translate", "annotate", "logic")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
CHECKED = {"section", "div", "article", "main", "header", "footer", "ul", "ol", "li", "table", "tr", "details", "dl", "p", "mark", "blockquote"}


class BalanceChecker(HTMLParser):
    """Report unclosed or stray structural tags — the usual cause of a broken two-column layout."""

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


def summarize(template: str, body: str) -> str:
    pairs = len(re.findall(r'class="pair(?:\s[^"]*)?"', body))
    numbered = len(re.findall(r'<section[^>]*\bid="p\d+"', body))
    parts = [f"{pairs} pair rows ({numbered} numbered paragraphs)"] if template != "logic" else []
    if template == "annotate":
        qs = sorted(set(re.findall(r'class="chip (q\d)"', body)))
        marks = len(re.findall(r"<mark\b", body))
        answers = len(re.findall(r'class="answer q\d', body))
        parts.append(f"legend {', '.join(qs) or 'none'}; {marks} highlights; {answers} answer cards")
        used = set(re.findall(r'<mark class="(q\d)"', body))
        missing = used - set(qs)
        if missing:
            parts.append(f"WARNING: marks use {sorted(missing)} but the legend lacks them")
    if template == "logic":
        nodes = len(re.findall(r'class="node ', body))
        steps = len(re.findall(r'class="step"', body))
        parts.append(f"{nodes} argument-map nodes; {steps} flow steps")
    return "; ".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--template", required=True, choices=TEMPLATES)
    ap.add_argument("--title", required=True, help="page title (plain text)")
    ap.add_argument("--body", required=True, nargs="+", help="one or more HTML fragment files, in order")
    ap.add_argument("--out", required=True, help="output .html path")
    args = ap.parse_args()

    tpl_path = ASSETS / f"{args.template}.html"
    if not tpl_path.exists():
        print(f"error: template not found: {tpl_path}", file=sys.stderr)
        return 2
    template = tpl_path.read_text(encoding="utf-8")

    chunks = []
    for p in args.body:
        path = Path(p)
        if not path.exists():
            print(f"error: body fragment not found: {path}", file=sys.stderr)
            return 2
        chunks.append(path.read_text(encoding="utf-8").strip())
    body = "\n\n".join(chunks)

    leftover = re.findall(r"\{\{[A-Z_]+\}\}", body)
    if leftover:
        print(f"warning: body contains unfilled placeholders: {sorted(set(leftover))}", file=sys.stderr)

    checker = BalanceChecker()
    checker.feed(body)
    problems = checker.finish()
    for msg in problems[:20]:
        print(f"warning: {msg}", file=sys.stderr)
    if len(problems) > 20:
        print(f"warning: ... and {len(problems) - 20} more", file=sys.stderr)

    page = template.replace("{{TITLE}}", html.escape(args.title, quote=False)).replace("{{BODY}}", body)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out} ({len(page):,} chars) - {summarize(args.template, body)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
