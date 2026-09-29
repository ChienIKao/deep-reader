#!/usr/bin/env python3
"""Package the skill folder into dist/deep-reader.zip for upload to Claude.ai / ChatGPT.

Usage:  python scripts/package.py
"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "deep-reader"
DIST = ROOT / "dist"


def main() -> None:
    DIST.mkdir(exist_ok=True)
    out = DIST / "deep-reader.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(SKILL.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                # keep the top-level folder: deep-reader/SKILL.md, deep-reader/assets/...
                zf.write(path, path.relative_to(SKILL.parent).as_posix())
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
