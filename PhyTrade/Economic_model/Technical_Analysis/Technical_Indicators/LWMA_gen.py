"""
This script enables computing the LWMA indicator. A linearly weighted moving average (LWMA) is a moving average calculation that more
heavily weights recent price data. The most recent price has the highest weighting, and each prior price has progressively less weight.
The weights drop in a linear fashion. LWMAs are quicker to react to price changes than simple moving averages (SMA) and exponential
moving averages (EMA).

Victor Guillet
11/28/2018
"""


class LWMA:
    def __init__(self, big_data, lookback_period=10, max_weight=1):
        """
        Generates an LWMA indicator instance

        :param big_data: BIGDATA class
        :param lookback_period: Lookback period to be used, if larger than dataslice length, dataslice length is used
        :param max_weight: Weight given to current day value
        """

        self.lookback_period = lookback_period
        self.lwma = []

        for i in range(len(big_data.data_slice)):
            # ------------------ Calculate close values falling in timeperiod_1 and 2
            lookback_period_close_values = []

            for j in range(self.lookback_period):
                lookback_period_close_values.append(big_data.data_close_values[big_data.data_slice_start_ind + i - j])

            # ---> Compute weights for each days based on max weight param and lookback period
            weights = [max_weight]
            for j in range(1, self.lookback_period-1):
                weights.append(max_weight-(max_weight/self.lookback_period)*j)
            weights.reverse()

            # ---> Compute weighted daily values
            weighted_values = []
            for j in range(self.lookback_period):
                weighted_values.append(lookback_period_close_values[j]*weights[j])

            self.lwma.append(sum(weighted_values)/sum(weights))

        print(self.lwma)


