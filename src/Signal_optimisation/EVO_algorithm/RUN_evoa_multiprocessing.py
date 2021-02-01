
################################################################################################################
"""
Used for running optimiser on multiple cores

!!! run script, not if __name__ == "__main__" !!!
"""

# Built-in/Generic Imports
import sys
from multiprocessing import Pool

# Own modules
from src.Settings.SETTINGS import SETTINGS
from src.Signal_optimisation.EVO_algorithm.EVO_algorithm import EVO_algorithm

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


def optimise(ticker, *args):
    try:
        settings = SETTINGS()
        settings.market_settings.gen_market_settings()
        settings.fetch_dates(1)
        EVO_algorithm(settings, ticker, optimiser_setting=1)
    except:
        pass


if __name__ == "__main__":
    settings = SETTINGS()
    settings.market_settings.gen_market_settings()
    proccesses = 5   # Number of processes to create

    print(settings.market_settings.tickers)

    pool = Pool(proccesses)
    pool.map(optimise, settings.market_settings.tickers)

    print("List processing complete.")
    sys.exit()
