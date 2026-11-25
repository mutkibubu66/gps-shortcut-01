#!/usr/bin/env python3
"""GPS excuse entry for make.fun.

The program holds the GPS's one-line excuse for sending the driver down
the wrong road, checks it against the bounty gate, and drops it into
/output/entry.txt for the grader. Standard library only; no network.
"""

import os
import sys

ENTRY_PATH = "/output/entry.txt"
MAX_CHARS = 200


def excuse() -> str:
    """The GPS speaks for itself: the shortcut was real, the lake was not."""
    first_half = "That dirt road WAS a shortcut \u2014 it just shortcuts straight "
    second_half = "into a lake, and the map never mentioned the lake part."
    return first_half + second_half


def check(line: str) -> list:
    """Collect every gate violation; an empty list means the line is good.
    The gate is the bounty text: one line, at most 200 characters."""
    problems = []
    if line != line.strip():
        problems.append("leading or trailing whitespace")
    if len(line.splitlines()) != 1:
        problems.append("must be exactly one line")
    if not 1 <= len(line) <= MAX_CHARS:
        problems.append("must be 1-200 characters")
    if not line.strip():
        problems.append("must not be blank")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("must be valid UTF-8")
    return problems


def save(line: str) -> None:
    """Write the line out, then read it back and confirm it matches."""
    folder = os.path.dirname(ENTRY_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(ENTRY_PATH, "w", encoding="utf-8") as handle:
        handle.write(line + "\n")
    with open(ENTRY_PATH, encoding="utf-8") as handle:
        stored = handle.read()
    if stored != line + "\n":
        raise SystemExit("entry.txt does not match the line")


def run() -> int:
    """Validate, save, and print the excuse."""
    line = excuse()
    problems = check(line)
    if problems:
        print("gate failed: " + "; ".join(problems), file=sys.stderr)
        return 1
    save(line)
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
