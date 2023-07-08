#!/usr/bin/env python3
import chardet
import re
import mutagen
from pathlib import Path

cue_file_regex = re.compile(r'".+"')
exclude_dirs = []
base = Path.cwd()

music_type = [
    ".m4a",
    ".wav",
    ".tta",
    ".vob",
    ".flac",
    ".tak",
    ".ac3",
    ".aac",
    ".m4a",
    ".ape",
    ".vob",
    ".mp3",
]


def get_cue_content(p: Path) -> str:
    print(p)
    with open(p, "rb") as f:
        data = f.read()
        detres = chardet.detect(data)
        encoding = detres["encoding"]
        if encoding == "GB2312":
            encoding = "gbk"
            txt = data.decode(encoding=encoding, errors="ignore")
        elif detres["confidence"] < 0.7:
            print("                 ", detres)
            encoding = "gbk"
            txt = data.decode(encoding=encoding)
        else:
            txt = data.decode(encoding=encoding)
        return txt


def create_cue(p: Path, content: str):
    with open(p, "w", encoding="utf8") as f:
        f.write(content)


def convert_path(rel_path: Path, s: str) -> str:
    if s.strip().startswith("FILE"):
        m = cue_file_regex.search(s)
        name = Path((m.group(0))[1:-1])
        res = '"' + str(rel_path.joinpath(name)) + '"'
        s = cue_file_regex.sub(res, s)
        print(s)
        return s
    else:
        return s


def rec(path: Path):
    if path.name == "mymusic":
        return
    paths = list(Path.iterdir(path))

    cues = list(filter(lambda p: p.suffix.lower() == ".cue", paths))
    dirs = list(filter(lambda p: p.is_dir(), paths))
    musics = list(
        filter(lambda p: p.is_file() and p.suffix.lower() in music_type, paths)
    )
    # print(dirs)
    if len(cues):
        for p in cues:
            content = get_cue_content(p)
            rel_path = Path("../..").joinpath(p.parent.relative_to(base))
            content = "\n".join(
                map(lambda s: convert_path(rel_path, s), content.splitlines())
            )
            dir_name = str(p.relative_to(base)).split("/")[0]
            print(dir_name)
            file_path = Path("mymusic").joinpath(dir_name).joinpath(p.name)
            if not file_path.parent.exists():
                Path.mkdir(file_path.parent, parents=True, exist_ok=True)
            create_cue(file_path, content)
    elif len(musics):
        new_cue_ctt = 'TITLE "' + path.name + '"\n'
        idx = 1
        musics.sort()
        for music in musics:
            print(f"meta_infos read in {music}")
            try:
                meta_infos = mutagen.File(music)
            except:
                meta_infos = None
            relpath = Path("../..").joinpath(music.relative_to(base))
            new_cue_ctt = new_cue_ctt + f'FILE "{relpath}" WAVE\n'
            new_cue_ctt = new_cue_ctt + f"  TRACK {idx:02} AUDIO\n"
            if meta_infos and "title" in meta_infos:
                new_cue_ctt = new_cue_ctt + f'    TITLE "{meta_infos["title"][0]}"\n'
            else:
                new_cue_ctt = new_cue_ctt + f'    TITLE "{music.stem}"\n'
            if meta_infos and "artist" in meta_infos:
                new_cue_ctt = new_cue_ctt + f'    PERFORMER "{" / ".join(meta_infos["artist"])}"\n'
            new_cue_ctt = new_cue_ctt + "    INDEX 01 00:00:00\n"
            idx += 1
        file_name = musics[0].parent.name + '.cue'
        dir_name = str(musics[0].relative_to(base)).split("/")[0]
        file_path = Path("mymusic").joinpath(dir_name).joinpath(file_name)
        if not file_path.parent.exists():
            Path.mkdir(file_path.parent, parents=True, exist_ok=True)
        create_cue(file_path, new_cue_ctt)

    for d in dirs:
        rec(d)


if __name__ == "__main__":
    print(base)
    rec(base)
