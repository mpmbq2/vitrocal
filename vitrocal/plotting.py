"""Module for plotting extracted events.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_events(events_df, roi=0, title='Detected Events for ROI', xlab='Time (s)', ylab='dF/F',
    color='C0', ax=None):

    """
    Plots the detected events for a given ROI.

    Args:
        events_df (DataFrame): A DataFrame with columns 'roi', 'time', and 'flourescence'.
        roi (int): The region of interest to plot.
        title (str): The title of the plot.
        xlab (str): The label for the x-axis.
        ylab (str): The label for the y-axis.
        color (str): The color of the line.
        ax (Axes): The axes to plot on. If None, a new figure is created.
    """

    if ax is None:
        fig, ax = plt.subplots()

    events = events_df[events_df['roi'] == roi]

    ax.plot(events['index'], events['flourescence'], color=color)

    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    ax.set_title(title + ' ' + str(roi))


def plot_average_event(combined, title='Average Detected Event', ylabel='df/F', 
                xlabel='Time', line_color='black', fill_color='C0', ax=None):

    """
    Plots the average detected event with the 25th and 75th percentiles shaded in.

    Args:
        combined (DataFrame): A DataFrame with columns 'median', 'q1', and 'q3'.
        title (str): The title of the plot.
        ylabel (str): The label for the y-axis.
        xlabel (str): The label for the x-axis.
        line_color (str): The color of the line.
        fill_color (str): The color of the fill.
        ax (Axes): The axes to plot on. If None, a new figure is created.
    """

    if ax is None:
        fig, ax = plt.subplots()

    ax.plot(combined.index, combined['median'], linestyle='dashed', color=line_color)
    ax.fill_between(combined.index, combined['q1'], combined['q3'], alpha=.25, color=fill_color)

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    ax.set_yticks([])
    ax.set_xticks([])