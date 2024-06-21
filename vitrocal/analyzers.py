import pandas as pd
import numpy as np

from .base import BaseAnalyzer

class StandardAnalyzer(BaseAnalyzer):
    def __init__(self,
                 upper_decay_bound: float=0.8,
                 lower_decay_bound: float=0.2):
        
        self.upper_decay_bound = upper_decay_bound
        self.lower_decay_bound = lower_decay_bound
        
        """
        Initialize analyzer object.

        Parameters
        ----------
        upper_decay_bound, lower_decay_bound : float
            Proprtion of peak fluoresence from which to calculate decay.

        Returns
        -------
        DataFrame with values for each ROI-event combination.
        """

    def analyze(self, events) -> pd.DataFrame:

        decay = self.find_event_decay(events)
        results = pd.DataFrame()
        for roi, values in decay.items():
            tmp = pd.DataFrame(values)
            tmp.insert(0, 'roi', roi)

            results = pd.concat([results, tmp])

        return results

    def count_events(self, events) -> dict:
         return {k: len(v) for k, v in events.items()}
    
    def find_event_peaks(self, events) -> dict:
        return {k: [np.max(ev) for ev in v] for k, v in events.items()}
    
    def find_event_decay(self, events) -> dict:
        """
        Determine event peak and decay using thresholds.
        """
        def _handle_decay_values(x):
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

        

