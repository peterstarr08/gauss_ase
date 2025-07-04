import argparse
from gs.pipeline.file_handler import FileHandler

def arg_parse():
    parser = argparse.ArgumentParser(description="To check status of batches")
    parser.add_argument("--meta", type=str, required=True, help="Path to meta json")
    return parser.parse_args()

def main():
    args = arg_parse()
    print(FileHandler(meta_path=args.meta))

if __name__=="__main__":
    main()