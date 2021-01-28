
##################################################################################################################
"""
Used to generate the CCI indicator

https://blog.quantinsti.com/build-technical-indicators-in-python/#cci
"""

# Libs
import pandas as pd
import numpy as np

# Own modules
from PhyTrade.Economic_model.Technical_indicators.Technical_Indicators.Indicator_abc import Indicator_abc

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class CCI(Indicator_abc):
    def __init__(self, big_data, timeperiod=20):
        # --> CCI initialisation
        self.timeperiod = timeperiod

        # -------------------------- CCI CALCULATION ---------------------------
        # --> Slice data to obtain Data falling in data slice + timeframe
        cci_df = big_data.data_slice.data[big_data.data_slice.subslice_start_index-self.timeperiod:
                                          big_data.data_slice.subslice_stop_index]

        tp = (cci_df['High'] + cci_df['Low'] + cci_df['Close']) / 3

        cci = pd.Series((tp - tp.rolling(window=self.timeperiod, center=False).mean()) /
                        (0.015 * tp.rolling(window=self.timeperiod, center=False).std()), name='CCI')

        self.cci_values = np.array(cci.values[self.timeperiod:])

    """




    """
    # ===================== INDICATOR OUTPUT DETERMINATION ==============
    def get_output(self, big_data, include_triggers_in_bb_signal=False):
        from PhyTrade.Tools.Math_tools import Math_tools

        # ----------------- Bear/Bullish continuous signal
        self.bb_signal = self.cci_values

        # --> Normalising cci bb signal values between -1 and 1
        # self.bb_signal = Math_tools().normalise_minus_one_one(self.cci_values)
        self.bb_signal = Math_tools().alignator_minus_one_one(signal=self.bb_signal,
                                                              signal_max=150,
                                                              signal_min=-150)
