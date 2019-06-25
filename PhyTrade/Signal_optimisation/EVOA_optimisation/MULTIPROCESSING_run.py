from PhyTrade.Settings.SETTINGS import SETTINGS
from PhyTrade.Signal_optimisation.EVOA_optimisation.EVO_algo_4 import EVOA_optimiser

from multiprocessing import Pool


def optimise(ticker, *args):
    settings = SETTINGS()
    settings.market_settings.gen_market_settings()
    EVOA_optimiser(settings, ticker)


if __name__ == "__main__":
    settings = SETTINGS()
    settings.market_settings.gen_market_settings()
    procs = 5   # Number of processes to create

    print(settings.market_settings.tickers)

    pool = Pool(procs)
    pool.map(optimise, settings.market_settings.tickers)

    print("List processing complete.")
