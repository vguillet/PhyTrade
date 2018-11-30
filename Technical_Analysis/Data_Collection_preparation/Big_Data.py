"""
The big data class contains all the information relating to a specific analysis,
modules can be called, and their instance attribute should be saved in the big_data instance
(to enable attribute access anywhere).
To compute specific attributes, run the corresponding Indicators/modules. The list of all options
can be found in the PhyTrade Library file

Victor Guillet
11/28/2018
"""


class BIGDATA:
    def __init__(self, data, ticker, data_slice_start_ind=0, data_slice_stop_ind=200):
        import numpy as np

        self.ticker = ticker
        self.data = data
        self.dates = list(self.data.index.values)

        self.data_slice_start_ind = data_slice_start_ind
        self.data_slice_stop_ind = data_slice_stop_ind
        self.data_slice = data[data_slice_start_ind:data_slice_stop_ind]
        self.data_slice_dates = list(self.data_slice.index.values)

        self.sell_trigger_values = []
        self.buy_trigger_values = []

        self.sell_trigger_dates = []
        self.buy_trigger_dates = []

        # --------------------- List close/open values
        # ... in data
        self.data_open_values = []
        self.data_close_values = []

        for index, row in self.data.iterrows():
            self.data_close_values.append(row['Close'])
            self.data_open_values.append(row['Open'])

        # ... in data slice
        self.data_slice_open_values = []
        self.data_slice_close_values = []

        for index, row in self.data_slice.iterrows():
            self.data_slice_close_values.append(row['Close'])
            self.data_slice_open_values.append(row['Open'])

        # --------------------- List Volume values
        # ... in data slice
        self.volume = []
        for index, row in self.data_slice.iterrows():
            self.volume.append(row['Volume'])


        # ------- Calculate value fluctuation for each point in data slice
        values_fluctuation = []
        for i in range(len(self.data_slice)):
            values_fluctuation.append(self.data_slice_close_values[i] - self.data_slice_open_values[i])

        self.values_fluctuation = values_fluctuation

        # -------Calculate open/close values gradient:
        close_values_gradient = np.gradient(self.data_slice_close_values)
        open_values_gradient = np.gradient(self.data_slice_open_values)

        self.close_values_gradient = close_values_gradient
        self.open_values_gradient = open_values_gradient

        # -----------------Bear/Bullish continuous signal of dataset gradient
        avg_gradient = []
        avg_gradient_bb_signal = []

        # Obtaining the average gradient
        for i in range(len(self.data_slice)):
            avg_gradient.append(
                (self.close_values_gradient[i] + self.open_values_gradient[i]) / 2)

        # Normalising avg gradient values between -1 and 1
        for i in range(len(avg_gradient)):
            avg_gradient_bb_signal.append(-((avg_gradient[i]) / (max(max(avg_gradient), -min(avg_gradient)))))

        self.oc_avg_gradient_bb_signal = avg_gradient_bb_signal
