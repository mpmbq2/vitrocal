import pandas as pd

from .base import BasePreprocessor


class StandardPreprocessor(BasePreprocessor):

    def __init__(self, 
                 frames_per_second: int=None,
                 frame_rate: float=None,
                 filter_frequency: float=None,
                 bleach_period: int=None,
                 ):
        
        self.frames_per_second = frames_per_second
        self.frame_rate = frame_rate
        self.filter_frequency = filter_frequency
        self.bleach_period = bleach_period

    def filter(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def drop_frames(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def baseline(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def preprocess(self, data: pd.DataFrame) -> pd.DataFrame:

        data = self.drop_frames(data)
        data = self.filter(data)
        data = self.baseline(data)

        return data
