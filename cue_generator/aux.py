#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict

if __name__ == '__main__':
    a = defaultdict(int)
    while True:
        try:
            line = input()
            # print(Path(line).suffix)
            a[Path(line).suffix] += 1
        except EOFError:
            break
    print(a)