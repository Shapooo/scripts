#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup as bs
from pathlib import Path
from typing import Dict


def get_list(html_file: Path) -> Dict[int, str]:
    res = {}
    with open(html_file, "r") as f:
        soup = bs(f, "html.parser")
        links = soup.find_all("a", href=lambda x: x and x.startswith("details.php?"))
        for link in links:
            # 提取 href 属性值
            href = link["href"]

            # 提取 title 属性值
            title = link["title"]

            res[int(href.split("=")[1].split("&")[0])] = title
    return res


def main():
    if len(sys.argv) != 3:
        print(
            "This script check compeleted torrents that's not seeding. This works for tjupt"
        )
        print("Usage: get_not_seeding.py <seeding HTML> <completed HTML>")
        exit(1)

    seeding = get_list(Path(sys.argv[1]))
    completed = get_list(Path(sys.argv[2]))
    for comp_item in completed.items():
        if comp_item[0] not in seeding:
            id = comp_item[0]
            title = comp_item[1]
            print(f"https://tjupt.org/download.php?id={id} {title}")


if __name__ == "__main__":
    main()
