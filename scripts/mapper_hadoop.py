#!/usr/bin/env python3
import sys
for line in sys.stdin:
    parts = line.rstrip("\\n").split(",", 5)
    if len(parts) >= 5:
        print(parts[2].strip().upper() + "\\t1")
