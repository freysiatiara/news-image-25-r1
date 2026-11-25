#!/usr/bin/env python3
"""Copy the pre-drawn front page to the grader's output path.

Stdlib only. The image entry.png sits next to this file in the
repository; this program copies it byte for byte to the output
location and sets mode 0644. No network, no drawing, no randomness,
so both grader runs write identical bytes.
"""
import os
import shutil
import sys


def resolve_output():
    """Pick the output path, in the order the grader documents."""
    for var in ("ENTRY_OUTPUT", "OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        value = os.environ.get(var)
        if value:
            if var == "ENTRY_OUTPUT":
                return value
            return os.path.join(value, "entry.png")
    return "/output/entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    target = resolve_output()
    parent = os.path.dirname(target)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(source, target)
    os.chmod(target, 0o644)
    return 0


if __name__ == "__main__":
    sys.exit(main())
