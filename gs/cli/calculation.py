import argparse

def slurm_inter(args):
    ...

def arg_parse():
    parser = argparse.ArgumentParser("Calculation runner")
    subparsers = parser.add_subparsers(dest="action")

    slurm_parse = subparsers.add_parser('slurm', help="To start a batch calculation from auto-generated slurm scripts")
    slurm_parse.add_argument("--file", type=str, required=True, help="Path to meta file to begin calculations")
    slurm_parse.add_argument("--method",type=str, default="B3LYP", help="DFT method (default: B3LYP)")
    slurm_parse.add_argument("--basis",type=str, default="6-31G(d)", help="Basis set (default: 6-31G(d))")
    slurm_parse.set_defaults(func=slurm_inter)

    return parser.parse_args()

def main():
    args = arg_parse()
    args.func(slurm_inter)

if __name__=="__main__":
    main()