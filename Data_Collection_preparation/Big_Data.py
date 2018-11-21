"""
The big data class contains all the information relating to a certain analysis,
modules can be called, which then save all their outputs to the big_data instance
as new attributes. To compute specific attributes, run the corresponding modules:

Default |Attributes:
    D   ticker              : Ticker of the dataset
    D   data                : Data collected
    D   dates               : Dates of the data
    D   data_open_values    : Open values
    D   data_close_values   : Close values

    D   data_slice_start_ind: Starting index of data slice
    D   data_slice_stop_ind         : Stopping index of data slice
    D   data_slice                  : Data slice (data falling in range of the start/stop indices)
    D   data_slice_dates            : Dates of the data slice

    D   data_slice_close_values     : List of close values in data slice
    D   data_slice_open_values      : List of open values in data slice

RSI module:
    D   rsi_timeframe       : Time frame to be used by RSI module (default = 14)
    D   rsi_buffer_setting  : Buffer setting to be used by RSI module (default = 0)

        rsi_values          : RSI values for data slice
        rsi_upper_bound     : Dynamic upper bound for data slice
        rsi_lower_bound     : Dynamic lower bound for data slice

        rsi_sell_dates      : RSI trigger sell dates
        rsi_buy_dates       : RSI trigger buy dates

        rsi_sell_count      : RSI trigger sell count
        rsi_buy_count       : RSI trigger buy count

        rsi_sell_rsi        : RSI sell rsi
        rsi_buy_rsi         : RSI buy rsi

        rsi_bb_signal       : RSI bull-bear signal

OC module:
        rsi_sell_values     : sell values matching RSI sell triggers
        rsi_buy_values      : buy values matching RSI buy triggers

        data_slice_values_fluctuation       : Fluctuation of values in data

        data_slice_close_values_gradient    : Gradient of close values in data slice
        data_slice_open_values_gradient     : Gradient of open values in data slice

"""


class BIGDATA:
    def __init__(self, data, ticker, data_slice_start_ind, data_slice_stop_ind, timeframe_rsi=14, rsi_buffer_setting=0):

        self.ticker = ticker
        self.data = data
        self.dates = list(self.data.index.values)

        self.data_slice_start_ind = data_slice_start_ind
        self.data_slice_stop_ind = data_slice_stop_ind
        self.data_slice = data[data_slice_start_ind:data_slice_stop_ind]
        self.data_slice_dates = list(self.data_slice.index.values)

        # ---------------------List close/open values

        # ... in data
        self.data_open_values = []
        self.data_close_values = []

        for index, row in self.data.iterrows():
            # ...for the whole dataset
            self.data_close_values.append(row['Close'])
            self.data_open_values.append(row['Open'])

        # ... in data slice
        self.data_slice_open_values = []
        self.data_slice_close_values = []

        for index, row in self.data_slice.iterrows():
            # ...for the whole dataset
            self.data_slice_close_values.append(row['Close'])
            self.data_slice_open_values.append(row['Open'])

        # RSI data
        self.rsi_timeframe = timeframe_rsi
        self.rsi_buffer_setting = rsi_buffer_setting


