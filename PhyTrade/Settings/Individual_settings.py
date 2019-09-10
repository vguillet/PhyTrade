
##################################################################################################################
"""
Contains settings for generating individuals
"""

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class Individual_settings:
    # =============================== INDIVIDUAL GEN SETTINGS =====================
    def gen_individual_settings(self):
        self.spline_interpolation_factor = 4

        # ___________________________ Indicators count ___________________________
        self.rsi_count = 2
        self.sma_count = 2
        self.ema_count = 4
        self.lwma_count = 0
        self.cci_count = 3
        self.eom_count = 2

        # ___________________________ RSI parameters _____________________________
        self.rsi_buffer_setting = 0
        self.rsi_include_triggers_in_bb_signal = True

        # ___________________________ SMA parameters _____________________________
        self.sma_include_triggers_in_bb_signal = False

        # ___________________________ EMA parameters _____________________________
        self.ema_include_triggers_in_bb_signal = False

        # ___________________________ LWMA parameters ____________________________
        self.lwma_include_triggers_in_bb_signal = False

        # ___________________________ CCI parameters ____________________________
        self.cci_include_triggers_in_bb_signal = False

        # ___________________________ EOM parameters ____________________________
        self.eom_include_triggers_in_bb_signal = False

        # ___________________________ OC_GRADIENT parameters ____________________________
        self.oc_gradient_include_triggers_in_bb_signal = False

        # ___________________________ Threshold parameters _______________________
        self.threshold_type = ["Fixed value", "Bollinger bands size", "Bollinger bands/price diff"]
        self.threshold_setting = 2

        self.buffer_type = ["No buffer", "Fixed value buffer", "Google-trend based evolutive buffer"]
        self.buffer_setting = 1
