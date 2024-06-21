import pandas as pd
import numpy as np

from .base import BaseDetector, BaseExtractor

from typing import Tuple


class DerivativeDetector(BaseDetector):

    def __init__(self,
                 threshold: float=20,
                 frames_per_second: int=None):
        
        self.threshold = threshold
        # self.frames_per_second = frames_per_second
    """
    Initialize derivative detector object.

    Parameters
    ---------
    threshold : float
        Minimum percentile to identify an event.

    """  
        
    def detect(self, data):
        derivative = self._compute_derivative(data)
        return self._find_threshold_crossings(derivative)

    def _compute_derivative(self, data):
        kernel =  np.array([1, -1])
        kwargs = {'v': kernel, 'mode': 'same'}
        return data.apply(np.convolve, axis=0, **kwargs)

    def _find_threshold_crossings(self, data):
        def _detect_cross(s, threshold):
            # threshold_val = np.percentile(s, threshold)
            threshold_val = np.percentile(s[s>0], threshold)
            events = s.where(s > threshold_val)
            events[~np.isnan(events)] = 1
            return events

        kwargs = {'threshold': self.threshold}
        return data.apply(_detect_cross, **kwargs)


class StandardExtractor(BaseExtractor):

    def __init__(self,
                 window: Tuple[int],
                 frames_per_second: int=None,
                #  interframe_delay: float=None,
                 threshold: float=20):
        
        
        self.window = window
        self.frames_per_second = frames_per_second
        self.threshold = threshold
    """
    Initialize event extractor object.

    Parameters
    ---------
    window : Tuple[int]
        Backward and forward window in seconds defining an event.
    frames_per_second : float
    threshold : float
        Minimum percentile to identify an event. Passed to `BaseDetector()`


    Raises
    ------
    ValueError : Window size must be greater than interframe delay.

    """  

    def detect_and_extract(self, data) -> dict:
        detector = DerivativeDetector(threshold=self.threshold)
        detected = detector.detect(data)

        return self.extract(data, detected)

    def extract(self, data, detected) -> dict:
        identified = self._identify_events(data, detected)

        extracted_events = {}
        for column in data:
            roi = identified[column]
            events = np.split(roi, np.where(np.isnan(roi))[0])
            events = [ev[~np.isnan(ev)] for ev in events]
            events = [ev for ev in events if not ev.empty]

            extracted_events[roi.name] = events
        return extracted_events

    def _identify_events(self, data, detected):
        window = self._convert_window_to_frames()
        detected = (detected
                    .bfill(limit=window[0])
                    .ffill(limit=window[1])
        )
        return data[detected == 1]

    def _convert_window_to_frames(self):
        fps = self.frames_per_second
        return  tuple(int(w * fps) for w in self.window)
    
