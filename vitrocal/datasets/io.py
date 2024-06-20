import pandas as pd
from abc import ABC, abstractmethod
from pathlib import PurePosixPath


class AbstractDataset(ABC):
    @abstractmethod
    def load(self):
        return self._load()
    
    @abstractmethod
    def save(self):
        return self._save()