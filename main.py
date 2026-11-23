#!/usr/bin/env python3
"""Entrypoint for the news-image-20261123 entry.

The broadsheet image is rendered ahead of time by draw.py and committed
as entry.png next to this file. At grading time this script only copies
that committed file into the output directory, using the standard library
alone, so the run needs no extra packages, no fonts and no network.
"""

import os
import shutil
import sys
from pathlib import Path

IMAGE = "entry.png"


def output_dir():
    target = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = Path(target)
    path.mkdir(parents=True, exist_ok=True)
    return path


def main():
    here = Path(__file__).resolve().parent
    source = here / IMAGE
    if not source.is_file():
        print("error: %s is missing next to %s" % (IMAGE, __file__), file=sys.stderr)
        return 1
    dest = output_dir() / IMAGE
    shutil.copyfile(source, dest)
    if dest.stat().st_size != source.stat().st_size:
        print("error: copied file size does not match %s" % IMAGE, file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dest, dest.stat().st_size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
