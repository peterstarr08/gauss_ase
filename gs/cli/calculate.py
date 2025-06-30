# cli/run_dft.py
import argparse
from gs.calculator import start

def main():
    parser = argparse.ArgumentParser(description="Run DFT SPE + force calculations using Gaussian.")
    parser.add_argument("--input",type=str, required=True, help="Path to input file with multiple configs")
    parser.add_argument("--output",type=str, required=True, help="Path to output file for processed configs")
    parser.add_argument("--method",type=str, default="B3LYP", help="DFT method (default: B3LYP)")
    parser.add_argument("--basis",type=str, default="6-31G(d)", help="Basis set (default: 6-31G(d))")

    args = parser.parse_args()

    start(
        configs_path=args.input,
        out_path=args.output,
        method=args.method,
        basis=args.basis
    )

if __name__ == "__main__":
    main()
