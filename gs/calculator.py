from pathlib import Path

from ase.io import read, write
from ase.calculators.gaussian import Gaussian

from gs.log import get_logger

log = get_logger(__name__)


from pathlib import Path
from ase.io import read, write
from ase.calculators.gaussian import Gaussian
from gs.log import get_logger

log = get_logger(__name__)

def start(
        configs_path: str,
        out_path: str,
        method: str = "B3LYP",
        basis: str = "6-31G(d)",
):
    configs_path = Path(configs_path)
    out_path = Path(out_path)

    log.info("Reading configs from %s", configs_path)
    configs = read(configs_path, index=":")

    processed = []
    failed = []

    for i, atoms in enumerate(configs):
        log.info("Processing config %d/%d", i + 1, len(configs))

        try:
            atoms.calc = Gaussian(method=method, basis=basis, extra="Force")
            energy = atoms.get_potential_energy()
            forces = atoms.get_forces()

            atoms.info['energy_gauss'] = energy
            atoms.arrays['forces_gauss'] = forces
            atoms.calc = None

            log.info("Config %d: Energy = %.6f eV", i + 1, energy)
            log.info("Config %d: Forces =\n%s", i + 1, str(forces))

            processed.append(atoms)

        except Exception as e:
            log.warning("Failed to process config %d: %s", i + 1, str(e))
            failed.append(i)

    write(out_path, processed)
    log.info("Saved %d successfully processed configs to %s", len(processed), out_path)

    if failed:
        log.warning("Failed to process configs at indices: %s", failed)
