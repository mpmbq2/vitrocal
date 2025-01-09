"""Abstract dataset classes.
"""
from abc import ABC, abstractmethod


class AbstractDataset(ABC):
    """Abstract class for dataset."""
    @abstractmethod
    def load(self):
        """Loader base method."""
        return self._load()

    @abstractmethod
    def save(self):
        """Saver base method."""
        return self._save()
