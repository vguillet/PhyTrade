
##################################################################################################################
"""
Contain settings used by tradebots
"""

# Built-in/Generic Imports
import json

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class Tradebot_settings:
    # =============================== TRADEBOT SETTINGS ===========================
    def gen_tradebot_settings(self):
        tradebot_settings = json.load(open(r"C:\Users\Victor Guillet\Google Drive\Computer science\2-Programing\Repos\Python\Steffegium\Data\Settings\Current_settings\Tradebot_settings_.json"))

        # --> Simple investment settings
        self.s_initial_investment = tradebot_settings["s_initial_investment"]

        # --> Investment settings
        self.initial_investment = tradebot_settings["initial_investment"]

        self.fixed_investment = tradebot_settings["fixed_investment"]
        self.investment_percentage = tradebot_settings["investment_percentage"]

        self.asset_liquidation_percentage = tradebot_settings["asset_liquidation_percentage"]
