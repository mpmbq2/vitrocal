"""Module for analyzing extracted events.
"""
import numpy as np
import pandas as pd

from .base import BaseAnalyzer


class StandardAnalyzer(BaseAnalyzer):
    """Initialize analyzer object.

    Attributes:
        upper_decay_bound (float, optional): Proportion of data to denote
            upper bound. Defaults to 0.8.
        lower_decay_bound (float, optional): Proprtion of data to denote
            lower bound. Defaults to 0.2.
    """
    def __init__(self,
                 upper_decay_bound: float=0.8,
                 lower_decay_bound: float=0.2
    ):

        self.upper_decay_bound = upper_decay_bound
        self.lower_decay_bound = lower_decay_bound


    def analyze(self, events: dict, drop_inf=True) -> pd.DataFrame:
        """Return dataframe with event counts, peaks, and decay.

        Args:
            events (dict): Detected events from `StandardExtractor.detect_and_extract()`

        Returns:
            pd.DataFrame: Summary dataframe.
        """

        decay = self.find_event_decay(events)
        results = pd.DataFrame()
        for roi, values in decay.items():
            tmp = pd.DataFrame(values)
            tmp.insert(0, 'roi', roi)
            tmp = tmp.replace([np.inf, -np.inf], np.nan) # replace inf with missing

            results = pd.concat([results, tmp])

        avg_results = self.find_average_decay(results)

        return results, avg_results

    def count_events(self, events: dict) -> dict:
        """Count number of events for each trace.

        Args:
            events (dict): Detected events from `StandardExtractor.detect_and_extract()`

        Returns:
            dict: Counts.
        """

        return {k: len(v) for k, v in events.items()}

    def find_event_peaks(self, events: dict) -> dict:
        """Find peak for each event.

        Args:
            events (dict): Detected events from `StandardExtractor.detect_and_extract()`

        Returns:
            dict: Event peaks.
        """

        return {k: [np.max(ev) for ev in v] for k, v in events.items()}

    def find_event_decay(self, events: dict) -> dict:
        """Find event peaks and decay.

        Args:
            events (dict): Detected events from `StandardExtractor.detect_and_extract()`

        Returns:
            dict: Summary dictionary.
        """

        def _handle_decay_values(x: list) -> float:
            """Handle decay values.

            Args:
                x (list): Detected bounds.

            Returns:
                float: Single bound.
            """
            if len(x) >= 1:
                bound = x[0]
            else:
                bound = np.nan
            return bound

        summary = {}
        for roi, sequence in events.items():
            sequence_summary = []
            event_count = 1
            for event in sequence:
                peak = np.max(event)
                peak_index = np.argmax(event)

                upper_bound = peak * self.upper_decay_bound
                lower_bound = peak * self.lower_decay_bound

                upper_bounds = []
                lower_bounds = []

                for value in np.nditer(event[peak_index:]):

                    if value <= upper_bound and value > lower_bound:
                        upper_bounds.append(value)
                    if value <= lower_bound:
                        lower_bounds.append(value)

                upper = _handle_decay_values(upper_bounds)
                lower = _handle_decay_values(lower_bounds)

                res = {
                    'event': event_count,
                    'peak': peak,
                    'upper': upper,
                    'lower': lower,
                    'decay': upper - lower
                }
                event_count += 1

                sequence_summary.append(res)
            summary[roi] = sequence_summary

        return summary


    def find_average_decay(self, decay: pd.DataFrame) -> pd.DataFrame:
        """Return summary metrics for each event grouped by ROI.

        Args:
            decay (pd.DataFrame): Output from `StandardAnalyzer.find_event_decay()`

        Returns:
            pd.DataFrame: Average metrics per ROI.
        """

        agg_funcs = {
            'total_events': pd.NamedAgg(column='event', aggfunc='count'),
            'average_peak': pd.NamedAgg(column='peak', aggfunc='mean'),
            'average_decay': pd.NamedAgg(column='decay', aggfunc='mean')

        }
        avg = decay.groupby(['roi']).agg(
            total_events=agg_funcs['total_events'],
            average_peak=agg_funcs['average_peak'],
            average_decay=agg_funcs['average_decay']
        )

        return avg.reset_index()

    # def find_average_event(self, events: dict) -> pd.Series:
    #     """Index-wise average events.

    #     Args:
    #         events (dict): Detected events from `StandardExtractor.detect_and_extract()`

    #     Returns:
    #         pd.DataFrame: Index-wise average event.
    #     """
    #     combined = pd.Series()
    #     for trac, values in events.items():
    #         for sequence in values:
    #             tmp = pd.Series(sequence)
    #             combined = pd.concat([combined, tmp], axis=1).agg("mean", axis=1)

    #     return combined.sort_index()

    def find_average_event(self, events:dict) -> (pd.DataFrame, pd.DataFrame):
        """
        Find average events.
        
        Args:
            events: dictionary of events
        
        Returns:
            combined: combined dataframe of quantiles
            event_data: dataframe of events
        """

        # get maximum event duration
        max_length = 0
        for roi, data in events.items():
            for event in data:
                if len(event) > max_length:
                    max_length = len(event)


        # combine events into a single dataframe
        event_count = 0
        event_data = pd.DataFrame()

        for roi, data in events.items():
            for event in data:
                event = list(event)
                if len(event) < max_length:
                    event.extend([np.nan] * (max_length - len(event)))
                tmp = pd.DataFrame({'flourescence': event})
                tmp['index'] = range(len(tmp))
                tmp['roi'] = roi
                event_data = pd.concat([event_data, tmp], axis=0)
                event_count += 1

        
        def _aggregate_events(x: pd.DataFrame):
            q1 = x.quantile(.25)
            q3 = x.quantile(.75)
            median = x.median()
            mean = x.mean()

            combined = pd.concat([q1, q3, median, mean], axis=1)
            combined.columns = ['q1', 'q3', 'median', 'mean']

            return combined


        global_average = _aggregate_events(event_data.drop(columns='roi').groupby('index'))
        roi_average = _aggregate_events(event_data.groupby(['roi', 'index']))

        return global_average, roi_average.reset_index(), event_data