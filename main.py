"""Entry program for news-image-20261122.

Copies the repository's entry.png to the directory make.fun provides
($MAKEFUN_OUTPUT_DIR, falling back to /output when the variable is
unset). It uses only the standard library, touches no network, and
copies the file byte for byte, so repeated runs produce identical bytes.
"""

import os
import shutil
import sys
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        sys.stderr.write("entry.png missing next to main.py\n")
        return 1
    target = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target / "entry.png")
    print("copied entry.png to", target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
