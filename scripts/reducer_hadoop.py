#!/usr/bin/env python3
import sys
current, total = None, 0
for line in sys.stdin:
    key, value = line.rstrip("\\n").split("\\t")
    if current is not None and key != current:
        print(current + "\\t" + str(total))
        total = 0
    current = key
    total += int(value)
if current is not None:
    print(current + "\\t" + str(total))
