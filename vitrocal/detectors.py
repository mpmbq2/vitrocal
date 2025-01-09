"""Detector and extractor classes for event detection and extraction."""
from typing import Tuple

import numpy as np
import pandas as pd

from .base import BaseDetector, BaseExtractor


class DerivativeDetector(BaseDetector):
    """Initialize derivative detector object.

    Attributes:
        threshold (float, optional): Minimum threshold (percent) to identify
            an event. Defaults to 20.
    """

    def __init__(self,
                 threshold: float=20):
        self.threshold = threshold

    def detect(self, data: pd.DataFrame) -> pd.DataFrame:
        """Compute derivatives and detect threshold crossings.

        Args:
            data (pd.DataFrame): m (images) x n (trace) dataframe.

        Returns:
            pd.DataFrame: Indicator (Boolean) dataframe of the same dimensions as
                input data.
        """
        derivative = self._compute_derivative(data)
        return derivative > self.threshold

    def _compute_derivative(self, data: pd.DataFrame) -> pd.DataFrame:
        """Compute element-wise difference.

        Args:
            data (pd.DataFrame):  m (images) x n (trace) dataframe.

        Returns:
            pd.DataFrame: Derivative dataframe.
        """

        return data.diff()

class StandardExtractor(BaseExtractor):
    """Initialize event extractor object.

    Attributes:
        window (Tuple[int]): Backward and forward window in seconds
            defining an event.
        frames_per_second (int, optional): Image aquisition rate.. Defaults to None.
        threshold (float, optional):  Minimum percentile to identify an event.
            Passed to `BaseDetector()`. Defaults to 20.
    """

    def __init__(self,
                 window: Tuple[int],
                 frames_per_second: int=None,
                 threshold: float=20
    ):
        self.window = window
        self.frames_per_second = frames_per_second
        self.threshold = threshold


    def detect_and_extract(self, data: pd.DataFrame) -> dict:
        """Compute derivatives and extract events.

        Args:
            data (pd.DataFrame): m (images) x n (trace) dataframe.

        Returns:
            dict: Dictionary of events.
        """
        detector = DerivativeDetector(threshold=self.threshold)
        detected = detector.detect(data)

        return self.extract(data, detected)

    def extract(self, data: pd.DataFrame, detected: pd.DataFrame) -> dict:
        """Extract events using fixed window.

        Args:
            data (pd.DataFrame): m (images) x n (trace) dataframe.
            detected (pd.DataFrame): dataframe of detected events.

        Raises:
            ValueError: `data` and `detected` must be the of the same dimensions.

        Returns:
            dict: Extracted events.
        """
        if data.shape != detected.shape:
            raise ValueError("Data and event dataframes must be the same dimensions.")

        identified = self._identify_events(detected)
        window = self._convert_window_to_frames()

        extracted_events = {}

        for column in data.columns:

            event_starts = identified[column]
            roi = data[column]

            indices = event_starts[event_starts is True].index

            events = []
            for index in indices:

                min_idx = index - window[0]
                max_idx = index + window[1]

                start = min_idx if min_idx > 0 else 0
                stop = max_idx if max_idx < len(roi) else len(roi)

                events.append(roi.loc[start:stop])

            extracted_events[roi.name] = events

        return extracted_events

    def _identify_events(self, detected: pd.DataFrame):
        """Identify events (where derivative = 0).

        Args:
            detected (pd.DataFrame): Dataframe

        Returns:
            pd.DataFrame: Dataframe of identified events.
        """

        identified = detected[detected.diff() != 0] # only keep start of event
        identified[identified is False] = np.NaN # non-events

        return detected

    def _convert_window_to_frames(self) -> Tuple[int, int]:
        """Convert window supplied in FPS to numbers of frames.

        Returns:
            Tuple[int, int]: Detection window expressed as numbers of frames
                backward and forward respectively.
        """
        fps = self.frames_per_second
        window = tuple(int(w * fps) for w in self.window)

        print((f"With FPS = {self.frames_per_second}, a window of "
               f"{self.window} seconds captures {window[0]} frame(s) "
               f"before and {window[1]} frame(s) after each event."))

        return window
