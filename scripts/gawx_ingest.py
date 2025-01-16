"""GAWX."""

import glob
import os
import subprocess
from datetime import datetime, timedelta, timezone


def main():
    """Go Main Go."""
    os.chdir("/mnt/gawx")
    for offset in [0, 1]:
        now = datetime.now(timezone.utc) - timedelta(hours=offset)
        for fn in glob.glob(f"0030_{now:%Y%m%d_%H}????.msg31"):
            ts = datetime.strptime(fn[5:20], "%Y%m%d_%H%M%S")
            cmd = [
                "pqinsert",
                "-f",
                "NEXRAD2",
                "-p",
                f"GAWX_{ts:%Y%m%d_%H%M%S}",
                fn,
            ]
            subprocess.call(cmd, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    main()
