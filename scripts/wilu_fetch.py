"""Download WILU data."""

import os
import socket
import subprocess
import sys

import requests

BASE = "http://wiu.edu/SevereWeather/radar/nexrad2/WILU/"
LOCAL = "/mnt/level2/raw/WILU/"


def make_request(url):
    """Safer."""
    try:
        return requests.get(url, timeout=10)
    except socket.timeout:
        print(f"socket.timeout for {url}")
    except Exception:
        try:
            return requests.get(url, timeout=10)
        except requests.exceptions.ReadTimeout:
            return None
        except Exception as exp:
            print(f"exception {exp} for {url}")
    sys.exit()


def main():
    """Go Main Go."""
    req = make_request(BASE + "dir.list")
    if req is None:
        return
    files = []
    for lnum, line in enumerate(req.text.split("\n")[::-1]):
        if len(files) > 1 or lnum > 20:
            break
        tokens = line.split()
        if len(tokens) != 2 or not tokens[1].startswith("WILU"):
            continue
        fn2 = tokens[1].strip()
        fn = tokens[1].strip()[:18]
        if os.path.isfile(LOCAL + fn):
            continue
        req2 = make_request(BASE + fn2)
        if req2 is None:
            return
        files.append(fn)
        with open(LOCAL + fn, "wb") as fh:
            fh.write(req2.content)

    if not files:
        return
    os.chdir(LOCAL)
    subprocess.call("/home/meteor_ldm/pyWWA/util/gr.csh WILU", shell=True)
    for fn in files:
        subprocess.call(f"pqinsert -i -f NEXRAD2 {fn}", shell=True)


if __name__ == "__main__":
    main()
