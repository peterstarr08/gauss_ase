from pathlib import Path
import re
from ase.io import read, write
from ase.calculators.gaussian import Gaussian

from gs.utils.log import get_std_logger, intro_ascii

log = get_std_logger(__name__)

def calculate(
        config_path: Path,
        out_path: Path,
        method: str,
        basis: str,
        mem: str = "100GB",
        nprocshared: int = 24,
        extra: list[str] = ["Force", "EmpiricalDispersion=GD2"]
):

    configs = read(config_path, index=":")
    log.info("Processing config %s      len=%d", str(config_path), len(configs))

    processed = []
    failed = []

    for i, atoms in enumerate(configs):
        log.debug("Processing config %d/%d", i + 1, len(configs))

        try:
            atoms.pbc = True
            atoms.calc = Gaussian(label=f'calc/{config_path.stem}' , mem=mem, nprocshared=nprocshared, method=method, basis=basis, extra=" ".join(extra))
            energy = atoms.get_potential_energy()
            forces = atoms.get_forces()

            atoms.info['energy_gauss'] = energy
            atoms.arrays['forces_gauss'] = forces
            atoms.calc = None

            log.info("Config %d: Energy = %.6f eV", i + 1, energy)
            # log.info("Config %d: Forces =\n%s", i + 1, str(forces))
            processed.append(atoms)

        except Exception as e:
            log.warning("Failed to process config %d: %s", i + 1, str(e))
            failed.append(i)

    if len(processed)>0:
            write(out_path, processed)
            log.info("Saved %d successfully processed configs to %s", len(processed), out_path)

    # if failed:
    #     log.warning("Failed to process configs at indices: %s", str(failed))

def entry(
        dir_path: str,
        method: str,
        basis: str,
        mem: str,
        nproc: int,
        extra: list[str]
):
    dir_path = Path(dir_path).resolve(strict=True)

    print(intro_ascii())

    gframe_files = list(dir_path.glob('gframe_*.xyz'))
    frame_files = list(dir_path.glob('frame_*.xyz'))

    # Extract numbers
    gframe_nums = {re.search(r'gframe_(\d+)\.xyz', f.name).group(1) for f in gframe_files}
    frames = [f for f in frame_files if re.search(r'frame_(\d+)\.xyz', f.name).group(1) not in gframe_nums]
        
    log.info("Processing %d frames from %s", len(frames), str(dir_path))

    for f in frames:
         calculate(config_path=f, out_path=f.with_name("g"+f.name), method=method, basis=basis, mem=mem, nprocshared=nproc, extra=extra)
    
    log.info("Done !!!")
