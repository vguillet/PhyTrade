
##################################################################################################################
"""
Used for computing the EOM indicator. The Ease of Movement indicator is a technical study that attempts
to quantify a mix of momentum and volume information into one value.
"""

# Libs
import numpy as np

# Own modules
from PhyTrade.Economic_model.Technical_indicators.Technical_Indicators.Indicator_abc import Indicator_abc

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################

# TODO: Verify EOM (returning [-1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1. -1. -1.
#  -1. -1. -1. -1. -1. -1. -1.])


class EOM(Indicator_abc):
    def __init__(self, big_data, timeperiod=14):
        # --> EMV initialisation
        self.timeperiod = timeperiod

        # -------------------------- CCI CALCULATION ---------------------------
        # --> Slice data to obtain Data falling in data slice + timeframe
        eom_df = big_data.data_slice.data[big_data.data_slice.subslice_start_index-self.timeperiod:
                                          big_data.data_slice.subslice_stop_index]

        dm = ((eom_df['High'] + eom_df['Low'])/2) - ((eom_df['High'].shift(1) + eom_df['Low'].shift(1))/2)
        br = (eom_df['Volume'] / 100000000) / (eom_df['High'] - eom_df['Low'])
        eom = dm / br
        eom_values = eom.rolling(self.timeperiod, center=False).mean()

        self.eom_values = np.array(eom_values.values[self.timeperiod:])

    """




    """
    # ===================== INDICATOR OUTPUT DETERMINATION ==============
    def get_output(self, big_data, include_triggers_in_bb_signal=False):
        from PhyTrade.Tools.Math_tools import Math_tools

        # ----------------- Bear/Bullish continuous signal
        self.bb_signal = self.eom_values

        # --> Normalising eom bb signal values between -1 and 1
        # self.bb_signal = Math_tools().normalise_minus_one_one(self.eom_values)
        self.bb_signal = Math_tools().alignator_minus_one_one(signal=self.bb_signal,
                                                              signal_max=5,
                                                              signal_min=-5)

