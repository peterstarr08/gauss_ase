# Param:
#
# gs.cli.file prepare
# --file: path to input file
# --count (1): number of batches to split
# --dir ('output'): output directory
# 
# Generates count number of subdirecoty batches in output directory
# containing all the .xyz files needed to be calcaulted. Contains
# .sh slurm script files to execute along with all log files
#
#
# gs.cli.file accimulate
# --dir ('output'): directory to output from 'prepare' cli
#
# Generates single configuration from all configuration inside this directory

import argparse
from gs.pipeline import preparer, accumulator

def prepare_inter(args):
    preparer(
        file=args.file,
        count=args.count,
        dir=args.dir
    )

def accumulate_inter(args):
    accumulator(
        dir_path=args.dir,
        out_path=args.out
    )

def arg_parse():
    parser = argparse.ArgumentParser("Prepearing for calculations and extracting single configuration file")
    subparsers = parser.add_subparsers(dest="action")

    prep_parser = subparsers.add_parser('prepare', help="Preparing batch for calculations")
    prep_parser.add_argument('--file', type=str, required=True, help="Path to configurations")
    prep_parser.add_argument('--count', type=int, default=1, help="Number of splits")
    prep_parser.add_argument('--dir', type=str, required=True, help="Output directory name")
    prep_parser.add_argument('--mem', type=str, default="49GB", help="Memory to allocate")
    prep_parser.add_arguments('--nproc', type=int, default=24, help="NProcShared count")
    prep_parser.set_defaults(func=prepare_inter)

    acc_parser = subparsers.add_parser('accumulate', help="Accumulating all calcaulted finished files")
    acc_parser.add_argument('--dir', type=str, required=True, help="Output directory path of calcaultions")
    acc_parser.add_argument('--out', type=str, required=True, help="Path to final files")
    acc_parser.set_defaults(func=accumulate_inter)

    return parser.parse_args()

def main():
    args = arg_parse()
    args.func(args)

if __name__=="__main__":
    main()
