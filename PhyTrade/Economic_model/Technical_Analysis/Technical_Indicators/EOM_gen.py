from PhyTrade.Economic_model.Technical_Analysis.Technical_Indicators.ABSTRACT_indicator import ABSTRACT_indicator
import pandas as pd
import numpy as np


class EOM(ABSTRACT_indicator):
    def __init__(self, big_data, timeperiod=14):
        # --> EMV initialisation
        self.timeperiod = timeperiod

        # -------------------------- CCI CALCULATION ---------------------------
        # --> Slice data to obtain Data falling in data slice + timeframe
        eom_df = big_data.data_slice.data[big_data.data_slice.start_index-self.timeperiod:big_data.data_slice.stop_index]

        dm = ((eom_df['High'] + eom_df['Low'])/2) - ((eom_df['High'].shift(1) + eom_df['Low'].shift(1))/2)
        br = (eom_df['Volume'] / 100000000) / (eom_df['High'] - eom_df['Low'])
        eom = dm / br
        eom_values = pd.Series(pd.rolling_mean(eom, self.timeperiod), name='EMV')

        self.eom_values = np.array(eom_values.values[self.timeperiod:])

    """




    """
    # ===================== INDICATOR OUTPUT DETERMINATION ==============
    def get_output(self, big_data, include_triggers_in_bb_signal=False):
        from PhyTrade.Tools.MATH_tools import MATH_tools

        # ----------------- Bear/Bullish continuous signal