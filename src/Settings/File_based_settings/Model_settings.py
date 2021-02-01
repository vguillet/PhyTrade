
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
        model_settings = json.load(open(r"C:\Users\Victor Guillet\Google Drive\Computer science\2-Programing\Repos\Python\Steffegium\Data\Settings\Current_settings\model_settings_.json"))
        # ___________________________ Print/plot parameters ______________________
        self.print_trade_process = model_settings["print_trade_process"]

        # ___________________________ Model parameters ___________________________
        self.evaluation_name = model_settings["evaluation_name"]

    # =============================== ECONOMIC MODEL SETTINGS =====================
    def gen_model_settings(self):
        # ___________________________ Modulation parameters ______________________
        # TODO: Add to evoa algo
        self.volume_std_dev_max = 3
        self.volatility_std_dev_max = 3
        self.buffer = 0.05
