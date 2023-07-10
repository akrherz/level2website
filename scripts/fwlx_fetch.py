"""Download FWLX data @DualDoppler."""
import os
import socket
import subprocess
import sys

import requests

BASE = "http://12.180.92.9/Output/FWLX/"
LOCAL = "/mnt/level2/raw/FWLX/"


def make_request(url):
    """Safer."""
    try:
        return requests.get(url, timeout=20)
    except socket.timeout:
        print(f"socket.timeout for {url}")
    except Exception as exp:
        print(f"exception {exp} for {url}")
    sys.exit()


def main():
    """Go Main Go."""
    req = make_request(BASE + "dir.list")
    files = []
    for line in req.text.split("\n")[::-1][:20]:
        tokens = line.split()
        if len(tokens) != 2 or not tokens[1].startswith("2008"):
            continue
        fn = tokens[1].strip()
        if os.path.isfile(LOCAL + fn):
            continue
        req2 = make_request(BASE + fn)
        files.append(fn)
        with open(LOCAL + fn, "wb") as fh:
            fh.write(req2.content)

    if not files:
        return
    os.chdir(LOCAL)
    subprocess.call("/home/meteor_ldm/pyWWA/util/gr.csh FWLX", shell=True)
    for fn in files:
        subprocess.call(f"pqinsert -i -f NEXRAD2 {fn}", shell=True)


if __name__ == "__main__":
    main()
