from pathlib import Path
from ase.io import read, write
from gs.log import get_logger

log = get_logger(__name__)

def splitter(
        file_path: str,
        count: int,
        out_dir: str
):
    file_path = Path(file_path).resolve(strict=True)
    out_dir = Path(out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    confs = read(file_path, ':')
    total = len(confs)

    log.info("Read %d configurations from %s", total, file_path)

    if count > total:
        log.warning("Requested count (%d) is greater than available configs (%d). Truncating count.", count, total)
        count = total

    for i in range(count):
        out_file = out_dir / f"{i}.xyz"
        write(out_file, confs[i])
        log.info("Wrote config %d to %s", i, out_file)

    log.info("Successfully split %d configs into directory %s", count, out_dir)


def joiner(
        dir_path: str,
        out_path: str
):
    dir_path = Path(dir_path).resolve(strict=True)
    out_path = Path(out_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    xyz_files = sorted(dir_path.glob("*.xyz"), key=lambda f: int(f.stem))
    
    if not xyz_files:
        log.error("No .xyz files found in directory: %s", dir_path)
        return

    log.info("Found %d .xyz files in %s", len(xyz_files), dir_path)

    all_confs = []
    for file in xyz_files:
        confs = read(file, ':')
        all_confs.extend(confs)
        log.info("Read %d configs from %s", len(confs), file)

    write(out_path, all_confs)
    log.info("Wrote total %d configs to %s", len(all_confs), out_path)