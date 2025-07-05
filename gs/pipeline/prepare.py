from pathlib import Path
from gs.template.hpc_slurm import make_calculation_script
from gs.utils.log import get_std_logger, intro_ascii
from gs.utils.meta_file import save_json
from .utils import read_atoms, write_atoms, make_bins


log = get_std_logger(__name__)

def generate_folder_paths(dir_path: Path, range: list[tuple[int, int]]):
    paths = [dir_path/f'{r[0]}_{r[1]}' for r in range]
    return paths

def generate_path_and_scripts(dir_path: Path, range: list[tuple[int, int]]):
    paths = []
    scripts = []
    for r in range:
        path = dir_path/f'{r[0]}_{r[1]}.sh'
        (dir_path/"logs").mkdir(parents=True, exist_ok=True)
        scr =  make_calculation_script(
            job_name=f'G{r[0]}_{r[1]}',
            out_file=str(dir_path/"logs"/f'{r[0]}_{r[1]}.out'),
            err_file=str(dir_path/"logs"/f'{r[0]}_{r[1]}.err'),
            command=f"\n\ngauss-ase-calculation slurm --dir {dir_path/f'{r[0]}_{r[1]}'}"
            )
        paths.append(path)
        scripts.append(scr)
    return paths, scripts

def entry(
        file: str,
        count: int,
        dir: str
):  
    print(intro_ascii())
    log.info("Beginning system preparation")

    file_pth = Path(file).resolve(strict=True)
    dir_path = Path(dir).resolve()

    if dir_path.exists():
        log.critical(f"Directory '{dir_path}' already exists.")
        raise RuntimeError(f"Directory '{dir_path}' already exists.")
    
    dir_path.mkdir(parents=True, exist_ok=False)
    
    log.info("Folder created at %s", str(dir_path))


    # Working with configurations
    configs = read_atoms(file_pth)
    bins = make_bins(size=len(configs), num_bins=count)
    bins_path = generate_folder_paths(range=bins, dir_path=dir_path)

    conf_indx = 0
    for b, bpth in zip(bins, bins_path):
        log.info("Processing configuration from index %d to %d", b[0], b[1])
        for at in configs[b[0]:b[1]+1]:
            log.debug("Processing config[%d]", conf_indx)
            write_atoms(bpth/f'frame_{conf_indx}.xyz', [at])
            conf_indx+=1
    
    # Log file
    save_json(path=dir_path/"meta.json" ,range=bins, size=len(configs))

    # Generating slurm scripts
    paths, scripts = generate_path_and_scripts(dir_path=dir_path, range=bins)
    for p, s in zip(paths, scripts):
        with open(p, 'w') as f:
            f.write(s)
            log.info("Slurm script written %s", str(p))
    

    log.info("Done !!!")
    log.info("Bonus: Check for bash slurm submit scripts and modify if needed")