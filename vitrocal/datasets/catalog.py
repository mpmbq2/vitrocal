import yaml
from abc import ABC, abstractmethod
from importlib import import_module

class AbstractCatalog(ABC):
    
    @abstractmethod
    def parse_catalog(self):
        return self._parse_catalog()

    @abstractmethod
    def load(self):
        return self._load()

def _get_dataset_type(dataset):
    type_list = dataset['type'].rsplit('.', 1)
    type_path = type_list.pop(0) if len(type_list) > 1 else ""
    type_path = ''.join(['.', dataset['type']])
    type_name = type_list[0]
    module = import_module(type_path, package='vitrocal')
    return getattr(module, type_name)



class DataCatalog(AbstractCatalog):
    """Allows easy access to `conf/catalog.yaml`. Inspired by
     https://kedro.org. 
     """
    def __init__(self, fpath="../../conf/catalog.yaml"):
        self.fpath = fpath
        self.datasets = self.parse_catalog()

    def parse_catalog(self) -> dict:
        fpath = self.fpath
        with open (fpath, 'r') as file:
            catalog = yaml.safe_load(file)
        return catalog
    
    def load(self, dataset):
        _dataset = self.datasets[dataset]
        module = _get_dataset_type(_dataset)
        filepath = _dataset['filepath']
        load_args = _dataset['load_args']

        return module(filepath, load_args).load()