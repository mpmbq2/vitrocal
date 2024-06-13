from abc import ABC, abstractmethod


class BasePreprocessor(ABC):
    
    @abstractmethod
    def preprocess(self):
        raise NotImplementedError("You must override the preprocess method to use this class")


class BaseDetector(ABC):
    
    @abstractmethod
    def detect(self):
        raise NotImplementedError("You must override the preprocess method to use this class")


class BaseExtractor(ABC):
    
    @abstractmethod
    def extract(self):
        raise NotImplementedError("You must override the preprocess method to use this class")


class BaseAnalyzer(ABC):
    
    @abstractmethod
    def analyze(self):
        raise NotImplementedError("You must override the preprocess method to use this class")
