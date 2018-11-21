

class BIGDATA:
    def __init__(self, data, ticker, data_slice_start_ind, data_slice_stop_ind, timeframe_rsi=14, rsi_buffer_setting=0):

        self.ticker = ticker
        self.data = data
        self.dates = list(self.data.index.values)

        self.data_slice_start_ind = data_slice_start_ind
        self.data_slice_stop_ind = data_slice_stop_ind
        self.data_slice = data[data_slice_start_ind:data_slice_stop_ind]
        self.data_slice_dates = list(self.data_slice.index.values)

        # RSI data
        self.rsi_timeframe = timeframe_rsi
        self.rsi_buffer_setting = rsi_buffer_setting

        # ---------------------List close/open values
        self.close_values = []
        self.open_values = []

        # Collect open and close values in respective lists
        for index, row in self.data.iterrows():
            # ...for the whole dataset
            self.close_values.append(row['Close'])
            self.open_values.append(row['Open'])


