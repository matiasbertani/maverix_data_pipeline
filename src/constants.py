from pathlib import Path


ROOT_PATH = Path(__file__).resolve().parent.parent
DATABASE_PATH = ROOT_PATH / "database"
INPUT_PATH = ROOT_PATH / "input"
RESULTS_PATH = ROOT_PATH / "results"
VERIFICATION_PATH = ROOT_PATH / "verification"


if __name__ == "__main__":
    print("The root of the project is:")
    print(ROOT_PATH)
