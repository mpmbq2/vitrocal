import pandas as pd
import numpy as np

from pandas.api.indexers import FixedForwardWindowIndexer
from .base import BasePreprocessor


class StandardPreprocessor(BasePreprocessor):

    def __init__(self, 
                 frames_per_second: int=None,
                 frame_rate: float=None,
                 filter_frequency: float=None,
                 window_size: float=60,
                 bleach_period: float=60,
                 ):
        
        """
        Initialize image preprocessor object.

        Parameters
        ---------
        frames_per_second : float
        bleach_period : float 
            Initial length of aqusition sequence to drop due to excessive
            photobleaching.
        filter_frequency: float
            n percent of data within `window_size` to use as baseline
        window_size : float
            Time in seconds to use for filter window.

        """  
        
        self.frames_per_second = frames_per_second
        # self.frame_rate = frame_rate
        self.filter_frequency = filter_frequency
        self.window_size = window_size
        self.bleach_period = bleach_period

        
    def preprocess(self, data: pd.DataFrame) -> pd.DataFrame:

        data = self.drop_frames(data)
        # data = self.filter(data)
        baseline = self.baseline(data)
        d_f = self.compute_fluoresence_change(data, baseline)

        return d_f
    
    def drop_frames(self, data: pd.DataFrame) -> pd.DataFrame:
        """Drop frames for all ROIs."""

        n_frames = len(data)
        frame_times = np.arange(n_frames) * 1/self.frames_per_second
        initial_frames = len(frame_times[frame_times <= self.bleach_period])

        return (data
                .iloc[initial_frames:]
                .reset_index(drop=True)
        )

    def baseline(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Identify baseline fluoresence using a backward-looking rolling window.
        """
        window_frames = int(self.window_size * self.frames_per_second)

        # turn this into a FixedBackwardwindowIndexer by reversing the dataframe
        indexer = FixedForwardWindowIndexer(window_size=window_frames)
        rev_data = data.iloc[::-1]

        baseline = (rev_data
            .rolling(window=indexer, min_periods=1)
            .apply(np.percentile, kwargs={'q': self.filter_frequency})
        )
        return baseline.iloc[::-1]
    
    def compute_fluoresence_change(self, data: pd.DataFrame, 
                                   baseline: pd.DataFrame) -> pd.DataFrame:
        return (data - baseline) / baseline * 100
    
    def filter(self, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

