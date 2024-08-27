from AnalyzeSingle import *
from glob import glob

def list_files(dir: str | os.PathLike="../data/01_raw/") -> list:
    dir = os.path.join(dir, "*.xlsx")
    return glob(dir)

def run_batch(file_list: list) -> None:
    for file in file_list:
        run(fpath_in=file)


if __name__ == "__main__":
    files = list_files()
    run_batch(files)
