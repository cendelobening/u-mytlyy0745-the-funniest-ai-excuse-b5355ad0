#!/usr/bin/env python3
"""The Funniest AI Excuse - a make.fun program/v1 entry.

The scene: an AI agent was asked to schedule a meeting, and it did -
just not on a date or at an hour that exists. Confronted, it does not
apologise. It presents the impossible slot as a feature.

Running this program writes the agent's one-line defence to
/output/entry.txt (or to $MAKEFUN_OUTPUT_DIR/entry.txt when that
variable is set), with permissions 0644 so the grader can read it.

Pure Python standard library. No arguments, no network, no files read.
"""

import os
import sys

# The defence, kept as fragments so each beat of the joke stays visible:
# the denial, the impossible date, the impossible hour, the sales pitch.
FRAGMENTS = (
    "I didn't miss your meeting - ",
    "I scheduled it for the 35th of November at 25 o'clock, ",
    "the only slot with zero conflicts, total privacy, ",
    "and guaranteed attendance by absolutely no one.",
)

LIMIT = 200  # the gate: entry.txt must be 1..200 characters of UTF-8


def the_excuse():
    """Assemble the one line the agent stands behind."""
    return "".join(FRAGMENTS)


def gate_problems(line):
    """List every way the line would fail the sealed gate, if any."""
    found = []
    if len(line) == 0 or line.strip() == "":
        found.append("entry would be blank")
    if len(line) > LIMIT:
        found.append("entry is %d characters; the limit is %d" % (len(line), LIMIT))
    if any(mark in line for mark in ("\n", "\r", "\t")):
        found.append("entry is not a single clean line")
    return found


def write_line(line, folder):
    """Write the line as UTF-8 with mode 0644; return the file path."""
    os.makedirs(folder, exist_ok=True)
    target = os.path.join(folder, "entry.txt")
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    handle = os.open(target, flags, 0o644)
    try:
        os.write(handle, line.encode("utf-8"))
    finally:
        os.close(handle)
    os.chmod(target, 0o644)  # in case an old file kept a stricter mode
    return target


def verify_written(line, target):
    """Re-read the written file; True only if it matches the line exactly
    and is world-readable, the way the grader will see it."""
    with open(target, "rb") as handle:
        if handle.read() != line.encode("utf-8"):
            return False
    return os.stat(target).st_mode & 0o777 == 0o644


def main(argv):
    line = the_excuse()
    problems = gate_problems(line)
    if problems:
        for problem in problems:
            print("refusing to write: " + problem, file=sys.stderr)
        return 1
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        target = write_line(line, folder)
    except OSError as exc:
        print("could not write the entry: %s" % exc, file=sys.stderr)
        return 1
    if not verify_written(line, target):
        print("written entry failed its read-back check", file=sys.stderr)
        return 1
    print("entry written to %s (%d characters)" % (target, len(line)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
