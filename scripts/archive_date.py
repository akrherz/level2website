"""Archive non-NEXRAD to some local storage.

Runs at about 6z for the previous UTC date
"""

import shutil
from datetime import timedelta
from pathlib import Path

from pyiem.util import logger, utc

LOG = logger()
RADARS_TO_ARCHIVE = (
    "FWLX FUSA GAWX WILU KULM MZZU DAN1 DOP1 FOP1 NOP3 NOP4 ROP3 ROP4 OP5R "
    "WILU ROK1 ROK2 ROK4 ROK5"
).split()
DEST_DIR = Path("/mnt/l2archive")
SRC_DIR = Path("/mnt/level2/raw")


def main():
    """Go Main Go."""
    dt = (utc() - timedelta(hours=12)).date()
    LOG.info("Processing date %s", dt)
    destdatedir = DEST_DIR / f"{dt:%Y/%m/%d}"
    if not destdatedir.exists():
        LOG.info("Creating %s", destdatedir)
        destdatedir.mkdir(parents=True)

    for radar in RADARS_TO_ARCHIVE:
        srcdir = SRC_DIR / radar
        if not srcdir.exists():
            LOG.info("Source %s does not exist, skipping", srcdir)
            continue
        found = False
        for fn in srcdir.glob(f"{radar}_{dt:%Y%m%d}*"):
            found = True
            destdir = destdatedir / radar
            if not destdir.exists():
                LOG.info("Creating %s", destdir)
                destdir.mkdir(parents=True)
            destfn = destdir / fn.name
            if destfn.exists():
                continue
            shutil.copyfile(fn, destfn)
        if not found:
            LOG.info("No files found for radar %s", radar)


if __name__ == "__main__":
    main()
