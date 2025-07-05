def make_calculation_script(
        job_name: str,
        out_file: str,
        err_file: str,
        command: str,
        prefix: str,
        N:int=1,
        mem:str ="100G",
        ntasks_per_node:int=24,
        time:str="24:00:00",
        partition:str="standard"
):
    '''Creates initial setup slurm script. Exporting paths and all. Scripts are needed to be added afterwards'''

    return(
        fr'''#!/bin/bash
#SBATCH -N {N}
#SBATCH --ntasks-per-node={ntasks_per_node}
#SBATCH --time={time}
#SBATCH --job-name={job_name}
#SBATCH --output={out_file}
#SBATCH --error={err_file}
#SBATCH --mem={mem}
#SBATCH --partition={partition}

# cd $SLURM_SUBMIT_DIR
# cd "$(dirname "$0")"
export GAUSS_EXEDIR=/home/apps/iiser/g09/g09
export PATH=$GAUSS_EXEDIR:$PATH

export ASE_GAUSSIAN_COMMAND="g09 < {prefix}.com > {prefix}.log"

{command}
'''
)