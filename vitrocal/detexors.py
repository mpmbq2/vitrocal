from .base import BaseDetector, BaseExtractor

from typing import Tuple


class DerivativeDetector(BaseDetector):

    def __init__(self,
                 threshold: float=0.2,
                 frames_per_second: int=None):
        
        self.threshold = threshold
        self.frames_per_second = frames_per_second
    
    def detect(self, data):
        pass

    def _compute_derivative(self, data):
        pass

    def _find_threshold_crossings(self, data):
        pass


class StandardExtractor(BaseExtractor):

    def __init__(self,
                 window: Tuple[int],
                 frames_per_second: int=None):
        
        self.window = window
        self.frames_per_second = frames_per_second

    def extract(self):
        pass
