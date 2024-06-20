import pandas as pd
from pathlib import PurePosixPath

from vitrocal.datasets.io import AbstractDataset

class ExcelDataset(AbstractDataset):
    def __init__(self, filepath:str, load_args={}):
        self._filepath = PurePosixPath(filepath)
        self._load_args = load_args
    
    def load(self) -> pd.DataFrame:
        return pd.read_excel(self._filepath, **self._load_args)
    
    def save(self):
        raise(NotImplementedError)