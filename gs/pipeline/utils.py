from pathlib import Path
from ase.io import read, write
from gs.utils.log import get_std_logger

log = get_std_logger(__name__)

def read_atoms(path: Path):
    db = read(path, ':')
    log.info("Read %d configs from %s", len(db), str(path))
    return db

def write_atoms(path: Path, db: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    write(path, db)
    log.info("%d configs written to %s", len(db), str(path))

def make_bins(size, num_bins):
    log.debug("make_bins    size=%d num_bins=%d", size, num_bins)

    base = size // num_bins
    remainder = size % num_bins
    bins = []
    start = 0

    for i in range(num_bins):
        end = start + base - 1
        if i < remainder:
            end += 1
        bins.append((start, end))
        start = end + 1

    log.debug("bins = %s", str(bins))

    return bins