"""
The big data class contains all the information relating to a specific analysis,
modules can be called, and their instance attribute should be saved in the big_data instance
(to enable attribute access anywhere).
To compute specific attributes, run the corresponding Indicators/modules:

Default |Attributes:
    D   ticker              : Ticker of the dataset
    D   data                : Data collected
    D   dates               : Dates of the data
    D   data_close_values   : List of close values in data slice
    D   data_open_values    : List of open values in data slice

    D   data_slice_start_ind        : Starting index of data slice
    D   data_slice_stop_ind         : Stopping index of data slice
    D   data_slice                  : Data slice (data falling in range of the start/stop indices)
    D   data_slice_dates            : Dates of the data slice
    D   data_slice_close_values     : List of close values in data slice
    D   data_slice_open_values      : List of open values in data slice

    D   values_fluctuation          : Fluctuation of values in data slice
    D   close_values_gradient       : Gradient of close values in data slice
    D   open_values_gradient        : Gradient of open values in data slice

    D   oc_avg_gradient_bb_signal   : OC gradient bull-bear signal

    D   sell_trigger_values         : Sell values matching sell triggers (initially empty list, to fill using calc_trigger_values from OC module)
    D   buy_trigger_values          : Buy values matching sell triggers (initially empty list, to fill using calc_trigger_values from OC module)

---------------------------------- Indicators (to be set as big_data attributes) ---------
RSI indicator:
        timeframe           : Time frame to be used by RSI module (default = 14)
        buffer_setting      : Buffer setting to be used by RSI module (default = 0)

        rsi_values          : RSI values for data slice
        upper_bound         : Dynamic upper bound for data slice
        lower_bound         : Dynamic lower bound for data slice

        sell_dates          : RSI trigger sell dates
        buy_dates           : RSI trigger buy dates

        sell_trigger_count  : RSI trigger sell count
        buy_trigger_count   : RSI trigger buy count

        sell_rsi            : RSI sell rsi
        buy_rsi             : RSI buy rsi

        bb_signal           : RSI bull-bear signal

    --> plot_rsi_and_bounds(self, big_data, plot_rsi=True, plot_upper_bound=True, plot_lower_bound=True, plot_trigger_signals=True):

SMA indicator:
        timeframe           : Time frame to be used by SMA module (default = 50)


---------------------------------- Tools -------------------------------------------------
OC module:
    --> calc_trigger_values(big_data, sell_dates, buy_dates):
            sell_trigger_values
            buy_trigger_values

    --> plot_open_close_values(big_data, plot_close_values=True, plot_open_values=True):

    --> plot_open_close_values_diff(big_data):

    --> plot_trigger_values(big_data):

SPLINE module:

        spline_x            : x value array for spline calculation
        spline_xs           : xs value array for spline calculation

    --> calc_signal_spline(big_data, signal, smoothing_factor=0.7):
            spline_length       : length of splines

    --> combine_signal_splines(big_data, signals):
            combined_signal_splines : combined selected signal spline
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
