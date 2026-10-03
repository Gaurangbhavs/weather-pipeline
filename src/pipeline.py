import sys

import extract
from load import load
from quality import run_all_checks
from transform import transform_all


def main():
    print("Step 1/4: extract")
    extract.main()

    print("Step 2/4: transform")
    df = transform_all()

    print("Step 3/4: quality checks")
    problems = run_all_checks(df)
    if problems:
        print("QUALITY CHECKS FAILED. Nothing was loaded.")
        for problem in problems:
            print(f"  - {problem}")
        sys.exit(1)
    print("All quality checks passed.")

    print("Step 4/4: load")
    load(df)

    print("Pipeline finished successfully.")


if __name__ == "__main__":
    main()