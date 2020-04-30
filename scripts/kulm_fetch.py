"""Download KULM data."""
import os
import subprocess

import requests

BASE = "http://wxdata.geos.ulm.edu/radar/KULM/"
LOCAL = "/mnt/level2/raw/KULM/"


def main():
    """Go Main Go."""
    req = requests.get(BASE + "dir.list", timeout=10)
    files = []
    for line in req.text.split("\n"):
        tokens = line.split()
        if len(tokens) != 2 or not tokens[1].startswith("KULM"):
            continue
        fn = tokens[1].strip()
        if os.path.isfile(LOCAL + fn):
            continue
        req2 = requests.get(BASE + fn, timeout=20)
        files.append(fn)
        with open(LOCAL + fn, "wb") as fh:
            fh.write(req2.content)

    os.chdir(LOCAL)
    subprocess.call("/home/meteor_ldm/pyWWA/util/gr.csh KULM", shell=True)
    for fn in files:
        subprocess.call("pqinsert -i -f NEXRAD2 %s" % (fn,), shell=True)


if __name__ == "__main__":
    main()
