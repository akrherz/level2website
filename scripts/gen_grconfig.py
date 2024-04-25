"""Look at our dirs and update the GRconfig."""

import glob
import os
from io import StringIO

BASEDIR = "/mnt/level2/raw"


def main():
    """Go Main Go."""
    os.chdir(BASEDIR)
    sio = StringIO()
    dirs = glob.glob("????")
    dirs.sort()
    for fn in dirs:
        if not os.path.isdir(fn):
            continue
        sio.write(f"Site: {fn}\n")
    with open("grlevel2.cfg", "w") as fp:
        fp.write(sio.getvalue())


if __name__ == "__main__":
    main()
