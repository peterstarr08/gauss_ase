import argparse
from gs.pipeline.file_handler import FileHandler

def arg_parse():
    parser = argparse.ArgumentParser(description="To check status of batches")
    parser.add_argument("--meta", type=str, required=True, help="Path to meta json")
    parser.add_argument("--prefix", type=str, required=True, choices=['o', 'g'], help="Prefix for calcaulted frame. o for orca, g for gaussian")
    return parser.parse_args()

def main():
    args = arg_parse()
    print(FileHandler(meta_path=args.meta, prefix=args.prefix))

if __name__=="__main__":
    main()