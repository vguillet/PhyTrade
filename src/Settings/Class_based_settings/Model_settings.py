
##################################################################################################################
"""
Contains settings for generating individuals
"""

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'
import json

##################################################################################################################


class Model_settings:
    # =============================== SINGLE TRADE SIM SETTINGS ===================
    def gen_run_model_settings(self):
        # ___________________________ Print/plot parameters ______________________
        self.print_trade_process = False

        self.plot_eco_model_results = True

        # ___________________________ Model parameters ___________________________
        self.evaluation_name = "1"

    # =============================== ECONOMIC MODEL SETTINGS =====================
    def gen_model_settings(self):
        # ___________________________ Modulation parameters ______________________
        # TODO: Add to evoa algo
        self.volume_std_dev_max = 3
        self.volatility_std_dev_max = 3
        self.buffer = 0.05
