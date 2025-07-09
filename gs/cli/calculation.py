import argparse
from gs.pipeline import gauss_calculator, orca_calculator


def gaussian_inter(args):
    gauss_calculator(
        dir_path=args.dir,
        method=args.method,
        basis=args.basis,
        mem=args.mem,
        nproc=args.nproc,
        extra=args.extra
    )

def orca_inter(args):
    orca_calculator(
        dir_path=args.dir,
        orcaPath=args.orca
    )

def arg_parse():
    parser = argparse.ArgumentParser("Calculation runner")
    subparsers = parser.add_subparsers(dest="action")

    gaussian_parse = subparsers.add_parser('gaussian', help="To begin calcaultion using Gaussian")
    gaussian_parse.add_argument("--dir", type=str, required=True, help="Path to directory")
    gaussian_parse.add_argument("--nproc", type=int, default=1, help="NProcShared value")
    gaussian_parse.add_argument("--mem", type=str, default="4GB", help="Memory allocation")
    gaussian_parse.add_argument("--method",type=str, default="B3LYP", help="DFT method (default: B3LYP)")
    gaussian_parse.add_argument("--basis",type=str, default="6-31G(d)", help="Basis set (default: 6-31G(d))")
    gaussian_parse.add_argument("--extra", type=str, nargs='+', default=["Force", "EmpiricalDispersion=GD3BJ"], help="Route section. To add forces or dispersion correction")
    gaussian_parse.set_defaults(func=gaussian_inter)
    
    
    orca_parse = subparsers.add_parser('orca', help="To begin calcaultion using Orca")
    orca_parse.add_argument("--dir", type=str, required=True, help="Path to directory")
    orca_parse.add_argument("--orca", type=str, required=True, help="Path to orca directory")
    orca_parse.set_defaults(func=orca_inter)
    return parser.parse_args()

def main():
    args = arg_parse()
    args.func(args)

if __name__=="__main__":
    main()
