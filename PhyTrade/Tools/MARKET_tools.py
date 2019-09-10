
################################################################################################################
"""
Contain market specific tools
"""

# Own modules
from PhyTrade.Settings.SETTINGS import SETTINGS

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class MARKET_tools:
    def calc_transaction_cost(self, asset_count):
        settings = SETTINGS()
        settings.market_settings.gen_market_settings()

        transaction_cost = asset_count*settings.market_settings.transaction_cost_per_share
        if transaction_cost < settings.market_settings.min_transaction_cost:
            transaction_cost = settings.market_settings.min_transaction_cost

        return transaction_cost
