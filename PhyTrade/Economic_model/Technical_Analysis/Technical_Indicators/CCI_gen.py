"https://blog.quantinsti.com/build-technical-indicators-in-python/#cci"

import pandas as pd


class CCI_gen:
    def __init__(self, big_data, timeperiod=12):
        # --> CCI initialisation
        self.timeperiod = timeperiod

        # -------------------------- CCI CALCULATION ---------------------------
        # --> Slice data to obtain Data falling in data slice + timeframe
        cci_df = big_data.data_slice.data[big_data.data_slice.start_index-self.timeperiod:big_data.data_slice.stop_index]

        tp = (cci_df['High'] + cci_df['Low'] + cci_df['Close']) / 3

        cci = pd.Series((tp - tp.rolling(window=self.timeperiod, center=False).mean()) /
                        (0.015 * tp.rolling(window=self.timeperiod, center=False).std()), name='CCI')

        print(cci.values[self.timeperiod:])
