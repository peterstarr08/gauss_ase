import argparse

from gs.files import splitter, joiner

def split_inter(args):
    splitter(
        file_path=args.file,
        count=args.count,
        out_dir=args.out
    )

def join_inter(args):
    joiner(
        dir_path=args.dir,
        out_path=args.out
    )

def arg_parse():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="handler")

    split_parser = subparsers.add_parser('split', help="Splits single .xyz to multiple .xyz")
    split_parser.add_argument('--file', type=str, required=True, help='Path to file')
    split_parser.add_argument('--count', type=int, default=1, help="How many splits to do")
    split_parser.add_argument('--out', type=str, required=True, help="Direcroty to put the split files into")
    split_parser.set_defaults(func=split_inter)

    join_parser = subparsers.add_parser('join', help="Joins multiple .xyz tp single .xyz")
    join_parser.add_argument('--dir', type=str, required=True, help="Directory to get all .xyz. Does recursively")
    join_parser.add_argument('--out', type=str, required=True, help="Path to store file")
    join_parser.set_defaults(func=join_inter)

    return parser.parse_args()

def main():
    args = arg_parse()
    args.func(args)

if __name__=='__main__':
    main()