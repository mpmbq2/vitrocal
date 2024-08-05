import pandas as pd
import numpy as np

from pandas.api.indexers import FixedForwardWindowIndexer
from scipy.signal import bessel, filtfilt
from .base import BasePreprocessor


class StandardPreprocessor(BasePreprocessor):
    """Preprocessor object class.

    Attributes:
        frames_per_second (int, optional): Image aquisition rate. Defaults to None.
        filter_frequency (float, optional): 
            Lowpass filter frequency (Hz). Defaults to None.
        filter_order (int, optional): 
            Order passed to scipy.signal.bessel. Defaults to 1.
        window_size (float, optional): 
            Size of rolling window to construct baseline values. Defaults to 60.
        baseline_threshold (float, optional): 
            Threshold below which to define baseline values (proportion). 
            Defaults to None.
        bleach_period (float, optional): 
        Initial photobleaching period to be removed (seconds). Defaults to 60.

    """

    def __init__(self, 
                 frames_per_second: int=None,
                 filter_frequency: float=None,
                 filter_order: int=1,
                 window_size: float=60,
                 baseline_threshold: float=None,
                 bleach_period: float=60,
        ):
        
        self.frames_per_second = frames_per_second
        self.filter_frequency = filter_frequency
        self.filter_order = filter_order
        self.window_size = window_size
        self.baseline_threshold = baseline_threshold
        self.bleach_period = bleach_period

        
    def preprocess(self, data: pd.DataFrame) -> pd.DataFrame:
        """Drop frames, filter, baseline, and compute flouresence change.

        Args:
            data (pd.DataFrame): m (images) x n (trace) dataframe.

        Returns:
            pd.DataFrame: Flouresence change dataframe with thes same dimensions
                as input data.
        """

        data = self.drop_frames(data)
        data = self.filter(data)
        baseline = self.baseline(data)
        d_f = self.compute_fluoresence_change(data, baseline)

        return d_f
    
    def drop_frames(self, data: pd.DataFrame) -> pd.DataFrame:
        """Drop frames for all traces.

        Args:
            data (pd.DataFrame): m (images) x n (trace) dataframe.

        Returns:
            pd.DataFrame: Dataframe with initial frames (rows) dropped.
        """

        n_frames = len(data)
        frame_times = np.arange(n_frames) * 1/self.frames_per_second
        initial_frames = len(frame_times[frame_times <= self.bleach_period])

        return (data
                .iloc[initial_frames:]
                .reset_index(drop=True)
        )
    
    def _construct_bessel_filter(self, filter_frequency:float, filter_order:int):
        """Apply scipy.signal.bessel filter.

        See https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.bessel.html # noqa

        Args:
            filter_frequency (float): Critical frequency.
            filter_order (int): Order of the filter.

        Returns:
            b,a: Numerator (b) and denominator (a) polynomials.
        """
        b, a = bessel(filter_order, filter_frequency)
        return b, a
    
    def filter(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply filter object backward and forward.

        Args:
            data (pd.DataFrame): ROI x image array.

        Returns:
            pd.DataFrame: Filtered output in the same shape as `data`.
        """

        if self.filter_frequency is None:
            print("No filter applied.")
            return data
        else:
            b, a = self._construct_bessel_filter(
                self.filter_frequency,
                self.filter_order
            )

            filtered = filtfilt(b, a, data)

            return pd.DataFrame(filtered)


    def baseline(self, data: pd.DataFrame) -> pd.DataFrame:
        """ Identify baseline fluoresence using a backward-looking rolling window.

        Args:
            data (pd.DataFrame): m (images) x n (trace) dataframe.

        Returns:
            pd.DataFrame: Dataframe with same dimensions as input data.
        """
        window_frames = int(self.window_size * self.frames_per_second)

        # turn this into a FixedBackwardwindowIndexer by reversing the dataframe
        indexer = FixedForwardWindowIndexer(window_size=window_frames)
        rev_data = data.iloc[::-1]

        baseline = (rev_data
            .rolling(window=indexer, min_periods=1)
            .apply(np.percentile, kwargs={'q': self.baseline_threshold})
        )
        return baseline.iloc[::-1]
    
    def compute_fluoresence_change(self, data: pd.DataFrame, 
                                   baseline: pd.DataFrame) -> pd.DataFrame:
        """Compute changfe in flouresence from baseline.

        `(data - baseline) / baseline * 100`

        Args:
            data (pd.DataFrame): m (images) x n (trace) input dataframe.
            baseline (pd.DataFrame): m (images) x n (trace) baseline dataframe.

        Returns:
            pd.DataFrame: Dataframe with same dimensions as input data.
        """
        return (data - baseline) / baseline * 100
    