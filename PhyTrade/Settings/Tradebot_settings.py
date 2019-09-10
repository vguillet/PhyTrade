
##################################################################################################################
"""
Contain settings used by tradebots
"""

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class Tradebot_settings:
    # =============================== TRADEBOT SETTINGS ===========================
    def gen_tradebot_settings(self):
        # --> Simple investment settings
        self.s_initial_investment = 1000

        # --> Investment settings
        self.fixed_investment = 100
        self.investment_percentage = 0.3

        self.asset_liquidation_percentage = 0.5
