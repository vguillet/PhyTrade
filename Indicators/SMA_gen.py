"""
This script enables computing the SMA indicator
It is currently optimised for Quandl data
"""


class SMA:
    def __init__(self, big_data, timeframe=50):
        self.timeframe = timeframe
