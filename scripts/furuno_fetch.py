"""Fetch FWLX and FUSA RADARs."""

import os
import subprocess
import sys

import click
import httpx

CONFIG = {
    "FWLX": "http://12.180.92.9/Output/FWLX",
    "FUSA": "http://50.238.124.10/Output/FUSA",
}
RADARID = {
    "FWLX": "2008",
    "FUSA": "2022",
}

LOCAL = "/mnt/level2/raw/"


def make_request(url):
    """Safer."""
    try:
        resp = httpx.get(url, timeout=10)
        resp.raise_for_status()
        return resp
    except Exception:
        pass
    sys.exit()


@click.command()
@click.option("--radar", default="FWLX", help="Radar to fetch.")
def main(radar: str):
    """Go Main Go."""
    radarid = RADARID[radar]
    req = make_request(f"{CONFIG[radar]}/dir.list")
    files = []
    for line in req.text.split("\n")[::-1][:20]:
        tokens = line.split()
        if len(tokens) != 2 or not tokens[1].startswith(radarid):
            continue
        fn = tokens[1].strip()
        lfn = fn.replace(f"{radarid}_20", f"{radar}_20")
        finalfn = f"{LOCAL}{radar}/{lfn}"
        if os.path.isfile(finalfn):
            continue
        req2 = make_request(f"{CONFIG[radar]}/{fn}")
        files.append(lfn)
        with open(finalfn, "wb") as fh:
            fh.write(req2.content)

    if not files:
        return
    os.chdir(LOCAL + radar)
    subprocess.call(["/home/meteor_ldm/pyWWA/util/gr.csh", radar])
    for fn in files:
        subprocess.call(["pqinsert", "-i", "-f", "NEXRAD2", fn])


if __name__ == "__main__":
    main()
