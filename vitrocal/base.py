"""Base classes."""
from abc import ABC, abstractmethod


class BasePreprocessor(ABC):
    """Base class for preprocessing data."""

    @abstractmethod
    def preprocess(self):
        """Base method for preprocessing data.

        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        raise NotImplementedError(
            "You must override the preprocess method to use this class")


class BaseDetector(ABC):
    """Base class for detecting events."""

    @abstractmethod
    def detect(self):
        """Base method for detecting events.

        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        raise NotImplementedError(
            "You must override the preprocess method to use this class")


class BaseExtractor(ABC):
    """Base class for extracting events."""

    @abstractmethod
    def extract(self):
        """Base method for extracting events.

        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        raise NotImplementedError(
            "You must override the preprocess method to use this class")


class BaseAnalyzer(ABC):
    """Base class for analyzing events."""

    @abstractmethod
    def analyze(self):
        """Base method for analyzing events.

        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        raise NotImplementedError(
            "You must override the preprocess method to use this class")
