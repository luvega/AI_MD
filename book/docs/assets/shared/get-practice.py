"""Download reviewed teaching files; requires only Python's standard library."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from urllib.request import urlopen, Request

BASE = "https://luvega.github.io/AI_MD/assets/"


def download(chapter: int, dest: Path, base: str = BASE) -> int:
    manifest_url = base.rstrip("/") + "/shared/practice-downloads.json"
    with urlopen(Request(manifest_url, headers={"User-Agent": "AI_MD-practice/1.0"}), timeout=60) as response:
        manifest = json.load(response)
    selected = {chapter}
    pending = [chapter]
    while pending:
        current = pending.pop()
        for dependency in manifest.get("dependencies", {}).get(str(current), []):
            if dependency not in selected:
                selected.add(dependency)
                pending.append(dependency)
    rows = [r for r in manifest["files"] if r["chapter"] in selected]
    if not rows:
        raise ValueError(f"No reviewed practice files for chapter {chapter}")
    root = dest.resolve()
    root.mkdir(parents=True, exist_ok=True)
    for row in rows:
        relative = PurePosixPath(row["relative_path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Invalid manifest path: {relative}")
        target = root.joinpath(*relative.parts).resolve()
        if root not in target.parents:
            raise ValueError(f"Path leaves download folder: {relative}")
        if target.is_file():
            if hashlib.sha256(target.read_bytes()).hexdigest() == row["sha256"]:
                print(f"Already downloaded: {relative}")
                continue
            raise FileExistsError(f"Keep your existing file or use a new destination: {target}")
        with urlopen(Request(base.rstrip("/") + "/" + row["url_path"], headers={"User-Agent": "AI_MD-practice/1.0"}), timeout=120) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise ValueError(f"Download checksum mismatch: {relative}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        print(f"Downloaded: {relative}")
    print("Included chapters:", ", ".join(str(n) for n in sorted(selected)))
    print("Practice root:", root)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter", type=int, choices=range(1, 13), required=True)
    parser.add_argument("--dest", type=Path, required=True)
    parser.add_argument("--base-url", default=BASE, help="Published asset base; useful for local preview")
    args = parser.parse_args()
    print(f"Ready: {download(args.chapter, args.dest, args.base_url)} files")


if __name__ == "__main__":
    main()
