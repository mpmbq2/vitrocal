"""Analyze batch of neuron output files.
"""
import os
from glob import glob

from AnalyzeSingle import run


def list_files(dir: str | os.PathLike="../data/01_raw/") -> list:
    """List files in a given directory.

    Args:
        dir (str | os.PathLike, optional): Directory. Defaults to "../data/01_raw/".

    Returns:
        list: List of files.
    """
    dir = os.path.join(dir, "*.xlsx")
    return glob(dir)

def run_batch(file_list: list) -> None:
    """Call `AnalyzeSingle.run()` for each file in a list.

    Args:
        file_list (list): List of file paths.
    """
    for file in file_list:
        run(fpath_in=file)


if __name__ == "__main__":
    files = list_files()
    run_batch(files)
