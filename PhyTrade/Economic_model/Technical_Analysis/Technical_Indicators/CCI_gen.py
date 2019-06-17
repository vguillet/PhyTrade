"https://blog.quantinsti.com/build-technical-indicators-in-python/#cci"
from PhyTrade.Economic_model.Technical_Analysis.Technical_Indicators.ABSTRACT_indicator import ABSTRACT_indicator
import pandas as pd
import numpy as np


class CCI(ABSTRACT_indicator):
    def __init__(self, big_data, timeperiod=12):
        # --> CCI initialisation
        self.timeperiod = timeperiod

        # -------------------------- CCI CALCULATION ---------------------------
        # --> Slice data to obtain Data falling in data slice + timeframe
        cci_df = big_data.data_slice.data[big_data.data_slice.start_index-self.timeperiod:big_data.data_slice.stop_index]

        tp = (cci_df['High'] + cci_df['Low'] + cci_df['Close']) / 3

        cci = pd.Series((tp - tp.rolling(window=self.timeperiod, center=False).mean()) /
                        (0.015 * tp.rolling(window=self.timeperiod, center=False).std()), name='CCI')

        self.cci_values = np.array(cci.values[self.timeperiod:])

    """




    """
    # ===================== INDICATOR OUTPUT DETERMINATION ==============
    def get_output(self, big_data, include_triggers_in_bb_signal=False):
        from PhyTrade.Tools.MATH_tools import MATH_tools

        # ----------------- Bear/Bullish continuous signal
        self.bb_signal = MATH_tools().normalise_minus_one_one(self.cci_values)
