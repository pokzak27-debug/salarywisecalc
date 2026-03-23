#!/usr/bin/env python3
"""Validate all internal links point to existing files."""

from pathlib import Path
import re

PROJECT = Path(__file__).parent.parent
EXISTING = set(p.name for p in PROJECT.glob("*.html"))

def extract_links(html):
    return set(re.findall(r'href="([^"]+\.html)(?:#[^"]*)?"', html))

broken = []
for path in PROJECT.glob("*.html"):
    html = path.read_text(encoding="utf-8")
    for href in extract_links(html):
        target = href.split("#")[0]
        if target not in EXISTING and not target.startswith("http"):
            broken.append((path.name, target))

if broken:
    for src, tgt in broken:
        print(f"BROKEN: {src} -> {tgt}")
    print(f"\n{len(broken)} broken links")
else:
    print("All internal links valid.")
