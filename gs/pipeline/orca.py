from pathlib import Path
import re
from ase.io import read, write
from ase.calculators.orca import OrcaProfile, ORCA

from gs.utils.log import get_std_logger, intro_ascii

log = get_std_logger(__name__)

def calculate(
        config_path: Path,
        out_path: Path,
        orcaPath: str,
        orcaInput: str,
        orcaNprocs: int 
):
    configs = read(config_path, index=":")
    log.info("Processing config %s      len=%d", str(config_path), len(configs))

    processed = []
    failed = []

    for i, atoms in enumerate(configs):
        
        log.debug("Processing config %d/%d", i + 1, len(configs))

        try:
            atoms.pbc = True

            profile = OrcaProfile(command=orcaPath)
            
            atoms.calc = ORCA(profile=profile, orcasimpleinput=orcaInput, orcablocks=f'%pal nprocs {orcaNprocs} end', directory=f'calc/{config_path.stem}')
             
            energy = atoms.get_potential_energy()
            forces = atoms.get_forces()

            atoms.info['energy_orca'] = energy
            atoms.arrays['forces_orca'] = forces
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
        orcaPath: str,
        orcaInput: str = "B3LYP D3BJ def2-TZVP TightSCF EnGrad",
        orcaNprocs: int = 24
):
    dir_path = Path(dir_path).resolve(strict=True)

    print(intro_ascii())

    oframe_files = list(dir_path.glob('oframe_*.xyz'))
    frame_files = list(dir_path.glob('frame_*.xyz'))

    # Extract numbers
    oframe_nums = {re.search(r'oframe_(\d+)\.xyz', f.name).group(1) for f in oframe_files}
    frames = [f for f in frame_files if re.search(r'frame_(\d+)\.xyz', f.name).group(1) not in oframe_nums]
        
    log.info("Processing %d frames from %s", len(frames), str(dir_path))

    for f in frames:
         calculate(config_path=f, out_path=f.with_name("o"+f.name), orcaPath=orcaPath, orcaInput=orcaInput, orcaNprocs=orcaNprocs)
    
    log.info("Done !!!")

   