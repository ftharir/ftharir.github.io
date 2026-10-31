"""Append translations given on stdin as '<number>|<Persian text>' lines to fa_vals.tsv."""
import os, sys
sys.stdin.reconfigure(encoding="utf-8")
out = os.path.join(os.path.dirname(__file__), "fa_vals.tsv")
with open(out, "a", encoding="utf-8", newline="\n") as f:
    n = 0
    for line in sys.stdin.read().splitlines():
        if "|" in line and line.split("|", 1)[0].strip().isdigit():
            a, b = line.split("|", 1)
            f.write(a.strip() + chr(9) + b + chr(10))
            n += 1
print("added", n)
