"""Entrypoint: copy the pre-rendered entry image to the Make.fun output directory.

Reads entry.png from this file's directory and writes it to
$MAKEFUN_OUTPUT_DIR/entry.png (default directory 'out' when the variable is
unset). Uses only the Python standard library. Deterministic: no network, no
randomness, no wall-clock time.
"""

import os
import shutil

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(base_dir, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    dst = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(src):
        raise FileNotFoundError("Missing source image: {}".format(src))

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)

    with open(dst, "rb") as fh:
        header = fh.read(len(PNG_MAGIC))
    if header != PNG_MAGIC:
        raise ValueError("Copied file does not start with PNG magic bytes")

    size = os.path.getsize(dst)
    print("wrote {} ({} bytes)".format(dst, size))


if __name__ == "__main__":
    main()
