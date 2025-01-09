"""ExcelDataset class definition"""
from pathlib import PurePosixPath

import pandas as pd

from vitrocal.datasets.io import AbstractDataset


class ExcelDataset(AbstractDataset):
    """ExcelDataset class."""
    def __init__(self, filepath:str, load_args={}):
        self._filepath = PurePosixPath(filepath)
        self._load_args = load_args

    def load(self) -> pd.DataFrame:
        """Loader function.

        Returns:
            pd.DataFrame: Dataframe.
        """
        return pd.read_excel(self._filepath, **self._load_args)

    def save(self):
        """Save function. Not yet implemented.
        """
        raise(NotImplementedError)
