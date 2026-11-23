# main.py — renders entry.png for news-image-20261123
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import draw

if __name__ == "__main__":
    out = "/output/entry.png"
    os.makedirs("/output", exist_ok=True)
    warns = draw.render(out)
    print("wrote", out)
    print("warnings: %d" % len(warns))
    for w in warns:
        print("  -", w)
