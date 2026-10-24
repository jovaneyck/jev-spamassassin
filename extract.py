"""Unpack the SpamAssassin corpus archives into dataset/<archive name>/.

Run:
    uv run extract.py     (once)
"""

import tarfile
from pathlib import Path

CORPUS = Path("dataset")


def main() -> None:
    for archive in sorted(Path().glob("*.tar.bz2")):
        target = CORPUS / archive.name.removesuffix(".tar.bz2")
        with tarfile.open(archive) as tar:
            members = [m for m in tar.getmembers() if "/" in m.name]
            for member in members:  # drop the archive's own top folder, e.g. easy_ham/
                member.name = member.name.split("/", 1)[1]
            tar.extractall(target, members=members, filter="data")
        print(f"{target}: {sum(1 for _ in target.iterdir())} files")


if __name__ == "__main__":
    main()
