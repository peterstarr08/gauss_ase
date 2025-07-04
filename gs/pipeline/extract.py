from pathlib import Path
import re
from gs.utils.log import get_std_logger, intro_ascii
from .utils import write_atoms, read_atoms

log = get_std_logger(__name__)

def entry(
        dir_path: str,
        out_path: str
):
    dir_path = Path(dir_path).resolve(strict=True)
    out_path = Path(out_path)


    print(intro_ascii())

    gframes = sorted(dir_path.rglob("gframe_*.xyz"), key=lambda f: int(re.search(r'\d+', f.name).group()))
    log.info("Found %d gaussian calculated frames", len(gframes))

    db = []

    for gfr in gframes:
        log.info("Processing %s", gfr.name)
        db+=read_atoms(gfr)
    
    write_atoms(out_path, db)
    log.info("Done !!!")