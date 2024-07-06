#!/usr/bin/env python3

import sys
from pathlib import Path
from typing import Set, List
from pprint import pprint


def collect_ref(ref_dir: Path) -> Set[str]:
    def helper(cur_dir: Path) -> List[str]:
        for item in cur_dir.iterdir():
            if item.is_dir():
                for ii in helper(item):
                    yield ii
            else:
                yield item.stem

    return set(helper(ref_dir))


def check_file(cur_dir: Path, ref_files: Set[str]) -> List[str]:
    if cur_dir.is_dir():
        for item in cur_dir.iterdir():
            if item.is_file():
                if item.stem in ref_files:
                    yield item
                else:
                    item.unlink()
            else:
                for i in check_file(item, ref_files):
                    yield i


def main():
    if len(sys.argv) != 3:
        print("This script output torrents that not in ref_dir")
        print("Usage: dedup.py <target_dir> <ref_dir>", file=sys.stderr)
        sys.exit(1)

    target_dir = Path(sys.argv[1])
    ref_dir = Path(sys.argv[2])

    ref_files = collect_ref(ref_dir)
    l = list(check_file(target_dir, ref_files))
    pprint(l)
    print(len(l))


if __name__ == "__main__":
    main()
