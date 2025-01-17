Welcome to the repository for the VitroCal project!

VitroCal is a Python-based toolbox for analyzing data collected through *in vitro*
calcium imaging. The package is designed to be flexible and user-friendly.

## Quickstart

<!-- uncomment if relevant
### Install from PyPI

```python
pip install vitrocal
```
-->
### Install from source

```bash
git clone git@github.com:mpmbq2/vitrocal.git
```

We recommend creating a virtual environment.

```bash
cd vitrocal
mamba env update -f environment.yml
conda activate vitrocal
python -m pip install .
```

## Example useage

```bash
datacatalog = catalog.DataCatalog()
df = datacatalog.load('data')
```
