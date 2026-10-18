#!/usr/bin/env python3
"""Removes the crowns and X marks from the graffiti. Run from the project root: python remove_crowns_x.py"""
import sys
from pathlib import Path

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "templates" / "home.html"
if not path.exists():
    sys.exit("Could not find templates/home.html (pass the path as an argument).")

html = path.read_text(encoding="utf-8")
changed = 0
for sig in ("function crown(x,y,rot,sz,col){", "function xm(x,y,s,col,sw){"):
    if sig not in html:
        sys.exit("Graffiti v3 code not found. Run update.py first.")
    if sig + "return '';" not in html:
        html = html.replace(sig, sig + "return '';", 1)
        changed += 1

path.write_text(html, encoding="utf-8")
print("Done." if changed else "Already removed.", path)