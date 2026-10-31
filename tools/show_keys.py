import sys
sys.stdout.reconfigure(encoding="utf-8")
import json, sys
k = [json.loads(x) for x in open(__import__("os").path.join(__import__("os").path.dirname(__file__), "fa_keys.jsonl"), encoding="utf8")]
a, b = int(sys.argv[1]), int(sys.argv[2])
for i in range(a, min(b, len(k)) + 1):
    print(f"{i}|{k[i-1]}")
