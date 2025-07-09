import argparse
from gs.pipeline import gauss_calculator

def slurm_inter(args):
    gauss_calculator(
        dir_path=args.dir,
        method=args.method,
        basis=args.basis,
        mem=args.mem,
        nproc=args.nproc
        extra=args.extra
    )

def arg_parse():
    parser = argparse.ArgumentParser("Calculation runner")
    subparsers = parser.add_subparsers(dest="action")

    slurm_parse = subparsers.add_parser('slurm', help="To start a batch calculation from auto-generated slurm scripts")
    slurm_parse.add_argument("--dir", type=str, required=True, help="Path to directory")
    slurm_parse.add_argument("--nproc", type=int, default=1, help="NProcShared value")
    slurm_parse.add_argument("--mem", type=str, default="4GB", help="Memory allocation")
    slurm_parse.add_argument("--method",type=str, default="B3LYP", help="DFT method (default: B3LYP)")
    slurm_parse.add_argument("--basis",type=str, default="6-31G(d)", help="Basis set (default: 6-31G(d))")
    slurm_parse.add_argument("--extra", type=str, args='+', default=["Force, EmpiricalDispersion=GD3BJ"], help="Route section. To add forces or dispersion correction")
    slurm_parse.set_defaults(func=slurm_inter)


    return parser.parse_args()

def main():
    args = arg_parse()
    args.func(args)

if __name__=="__main__":
    main()
