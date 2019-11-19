
################################################################################################################
"""
Used for running optimiser on multiple cores
"""

# Built-in/Generic Imports
from multiprocessing import Pool

# Own modules
from PhyTrade.Settings.SETTINGS import SETTINGS
from PhyTrade.Signal_optimisation.EVOA_optimisation.EVO_algo_4 import EVOA_optimiser

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


def optimise(ticker, *args):
    settings = SETTINGS()
    settings.market_settings.gen_market_settings()
    EVOA_optimiser(settings, ticker)


if __name__ == "__main__":
    settings = SETTINGS()
    settings.market_settings.gen_market_settings()
    proccesses = 5   # Number of processes to create

    print(settings.market_settings.tickers)

    pool = Pool(proccesses)
    pool.map(optimise, settings.market_settings.tickers)

    print("List processing complete.")
