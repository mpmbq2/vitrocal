import pandas as pd
import numpy as np
import os

from typing import Tuple
from vitrocal.datasets import ExcelDataset
from vitrocal.preprocessors import StandardPreprocessor
from vitrocal.detectors import StandardExtractor
from vitrocal.analyzers import StandardAnalyzer


def load_data(fpath: str | os.PathLike, load_args: dict=None) -> pd.DataFrame:
    """Load single neuron output file.

    Args:
        fpath (str | os.PathLike): Path to single Excel spreadsheet.
        load_args (dict, optional): Passed to `pd.read_excel()`. Defaults to None.

    Returns:
        pd.DataFrame: Dataframe
    """
    fname = os.path.basename(fpath)
    dataset = ExcelDataset.ExcelDataset(fpath)
    return dataset.load(), fname

def preprocess(df: pd.DataFrame, fps, bleach_period, filter_frequency,
               baseline_threshold, window_size
) -> pd.DataFrame:
    """Implement `vitrocal.preprocessors.StandardPreprocessor.load()`"""
    preprocessor = StandardPreprocessor(
        frames_per_second=fps,
        bleach_period=bleach_period,
        filter_frequency=filter_frequency,
        baseline_threshold=baseline_threshold,
        window_size=window_size
    )

    return preprocessor.preprocess(df)

def extract(df: pd.DataFrame, window, fps, threshold) -> dict:
    """Implement `vitrocal.detectors.StandardExtractor.detect_and_extract()`"""
    extractor = StandardExtractor(
        window=window,
        frames_per_second=fps,
        threshold=threshold
    )

    return extractor.detect_and_extract(df)

def analyze(events: dict, upper_decay_bound, lower_decay_bound) -> pd.DataFrame:
    """Implement `vitrocal.analyzers.StandardAnalyzer.analyze()`"""
    analyzer = StandardAnalyzer(
        upper_decay_bound=upper_decay_bound,
        lower_decay_bound=lower_decay_bound
    )

    return analyzer.analyze(events)

def save_data(df: pd.DataFrame, 
              fname: str | os.PathLike, 
              fpath: str | os.PathLike
) -> None:
    """Save analyzed events.

    Args:
        df (pd.DataFrame): Analyzed events.
        fname (str | os.PathLike): File name (with extension). 
            `.xlsx` will be coerced to `.csv`.
        fpath (str | os.PathLike, optional): File path. 
            Defaults to "../data/02_intermediate/".
    """
    
    # coerce .xlsx to csv
    excel_ext = ".xlsx"
    if excel_ext in fname:
        fname = fname.replace(excel_ext, ".csv")

    fpath = os.path.join(fpath, fname)
    df.to_csv(fpath, index=False)

def run(fpath_in: str | os.PathLike, fps: float=1/2.5, filter_frequency: float=None,
         preprocess_window_size: float=60,
        baseline_threshold: float=10, bleach_period: float=60,
        detection_window: Tuple[int]=(3, 30), detection_threshold: float=20,
        upper_decay_bound: float=0.8, lower_decay_bound: float=0.2,
        fpath_out: str | os.PathLike = "../data/02_intermediate/"
) -> None:
    """Produce analysis output for single input file.

    See `vitrocal` for details.
    """

    df, fname = load_data(fpath_in)
    df = preprocess(df, fps, bleach_period, filter_frequency, 
                    baseline_threshold, preprocess_window_size)
    extracted_data = extract(df, detection_window, fps, detection_threshold)
    analyzed_data = analyze(extracted_data, upper_decay_bound, lower_decay_bound)
    save_data(analyzed_data, fname, fpath_out)


if __name__ == "__main__":
    run(fpath_in="../data/01_raw/Fiji Neuron Output.xlsx")