"""Download KULM data."""
import json
import os
import subprocess

import requests
BASE = "http://wxdata.geos.ulm.edu/radar/KULM/"
LOCAL = "/mnt/level2/raw/KULM/"


def main():
    """Go Main Go."""
    secrets = json.load(open('kulm_secrets.json'))
    auth = (secrets['username'], secrets['password'])
    req = requests.get(BASE + "dir.list", auth=auth, timeout=10)
    files = []
    for line in req.text.split("\n"):
        tokens = line.split()
        if len(tokens) != 2 or not tokens[1].startswith("KULM"):
            continue
        fn = tokens[1].strip()
        if os.path.isfile(LOCAL + fn):
            continue
        req2 = requests.get(BASE + fn, auth=auth, timeout=20)
        files.append(fn)
        fp = open(LOCAL + fn, 'wb')
        fp.write(req2.content)
        fp.close()

    os.chdir(LOCAL)
    subprocess.call("/local/ldm/pyWWA/util/gr.csh KULM", shell=True)
    for fn in files:
        subprocess.call(
            "/local/ldm/bin/pqinsert -i -f NEXRAD2 %s" % (fn, ), shell=True)


if __name__ == '__main__':
    main()
