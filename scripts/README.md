# Single and Batch Analysis Scripts

Ready-made scripts to help with analyses. 

## Useage

Add arguments to`run()` in each file to your specifications. See function and `vitrocal`
documentation for examples:

```
def run(fpath_in: str | os.PathLike, fps: float=1/2.5, filter_frequency: float=None,
         preprocess_window_size: float=60,
        baseline_threshold: float=10, bleach_period: float=60,
        detection_window: Tuple[int]=(3, 30), detection_threshold: float=20,
        upper_decay_bound: float=0.8, lower_decay_bound: float=0.2,
        fpath_out: str | os.PathLike = "../data/02_intermediate/"
)
```

These scripts will automatically create analysis output files with the same names
as the input files. `AnalyzeBatch.py` calls `AnalyzeSingle.py` and repeats the analysis
for all files in a given directory. 

Example call:

```
conda activate vitrocal
python AnalyzeSingle.py
```
