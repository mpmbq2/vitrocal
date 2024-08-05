# Datasets module

Project datasets should be listed in `conf/catalog.yaml`. 

Example entry:

```
MyDataset:
  type: datasets.ExcelDataset
  filepath: ../../data/01_raw/my_dataset.xlsx
  load_args:
    header:
    index_col: 0
```

Access datsets from anywhere in the program using the `DataCatalog`:

```
from vitrocal.datasets import catalog
datacatalog = catalog.DataCatalog()

MyDataset = datacatalog.load('MyDataset')
```