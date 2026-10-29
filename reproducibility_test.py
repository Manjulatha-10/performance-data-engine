
import hashlib
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

FILES_TO_CHECK = [
    "managers.csv",
    "employees.csv",
    "review_cycles.csv",
    "goals.csv",
    "key_results.csv",
    "checkins.csv",
    "competencies.csv",
    "reviews.csv",
    "feedback.csv",
    "development_plans.csv",
]


def calculate_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def get_hashes():
    hashes = {}
    for filename in FILES_TO_CHECK:
        path = OUTPUT_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing file: {path}")
        hashes[filename] = calculate_hash(path)
    return hashes


def main():
    print("Generating full-scale dataset for the first run...")
    subprocess.run(
        [sys.executable, "generate_all.py", "--scale", "full"],
        cwd=BASE_DIR,
        check=True,
    )
    first_run = get_hashes()

    print("\nGenerating full-scale dataset for the second run...")
    subprocess.run(
        [sys.executable, "generate_all.py", "--scale", "full"],
        cwd=BASE_DIR,
        check=True,
    )
    second_run = get_hashes()

    print("\nReproducibility results:")
    all_match = True

    for filename in FILES_TO_CHECK:
        matches = first_run[filename] == second_run[filename]
        print(f"{filename}: {'MATCH' if matches else 'DIFFERENT'}")
        if not matches:
            all_match = False

    if all_match:
        print("\nPASS: All CSV files are reproducible.")
    else:
        print("\nFAIL: Some CSV files changed between runs.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
