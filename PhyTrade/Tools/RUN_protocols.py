
##################################################################################################################
"""
This class is used to run defined sequences of tasks.
"""

# Built-in/Generic Imports

# Libs

# Own modules
from PhyTrade.Settings.SETTINGS import SETTINGS
from PhyTrade.Tools.Colours_and_Fonts import cf

from PhyTrade.Signal_optimisation.EVOA_optimisation.EVO_algo_4 import EVOA_optimiser
from PhyTrade.Economic_model.RUN_model import RUN_model
from PhyTrade.Trade_simulations.RUN_single_trade_sim import RUN_single_trade_sim
from PhyTrade.Trade_simulations.RUN_multi_trade_sim import RUN_multi_trade_sim
from PhyTrade.Backtesting.Metalabeling.EVOA_METALABELS_gen import gen_ticker_metalabels

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '26/09/2019'

##################################################################################################################


class RUN_protocols:
    def __init__(self, task_sequence):
        self.task_sequence = task_sequence
        self.settings = SETTINGS()

        # --> Follow protocol
        available_tasks = ["--> EVOA Optimiser",
                           "--> EVOA Metalabeling",
                           "--> Economic analysis",
                           "--> Single ticker trade simulation",
                           "--> Multi ticker trade simulation"]

        print("\nInitiating protocol...\n\n\n\n\n\n\n\n")
        self.task_tracker = -1
        for task in self.task_sequence:
            self.task_tracker += 1
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Protocol Sequence ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            for i, task_nb in enumerate(self.task_sequence):
                if i == self.task_tracker:
                    print(cf["bold"] + cf["green"] + available_tasks[task_nb - 1] + cf["reset"])
                else:
                    print(available_tasks[task_nb - 1])
            print("\n")

            if task == 1:
                self.run_evoa_optimiser()

            if task == 2:
                self.run_evoa_metalabeling()

            if task == 3:
                self.run_economic_analysis()

            if task == 4:
                self.run_single_trade_simulation()

            if task == 5:
                self.run_multi_trade_simulation()

        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Protocol Completed ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # ============================ EVOLUTION-OPTIMISER =============================
    def run_evoa_optimiser(self):
        # --> Generate market settings
        self.settings.market_settings.gen_market_settings()

        def optimise(settings, ticker):
            try:
                settings.fetch_dates(1)
                EVOA_optimiser(settings, ticker, optimiser_setting=1)
            except:
                print(cf["red"] + "\n!!! Ticker ->", ticker, " <- invalid, moving to the next in the list !!!\n" + cf["reset"])

        for ticker in self.settings.market_settings.tickers:
            optimise(self.settings, ticker)

        # self.settings.fetch_dates(1)
        # EVOA_optimiser(self.settings, self.settings.market_settings.tickers[0], optimiser_setting=1)

    # ============================ EVOLUTION-METALABELING ==========================
    def run_evoa_metalabeling(self):
        # --> Generate market self.settings
        self.settings.market_settings.gen_market_settings()

        for ticker in self.settings.market_settings.tickers:
            gen_ticker_metalabels(self.settings, ticker)

    # ============================ ECONOMIC ANALYSIS ===============================
    @staticmethod
    def run_economic_analysis():
        RUN_model()

    # ============================ TRADING SIMULATIONS ==============================
    @staticmethod
    def run_single_trade_simulation():
        RUN_single_trade_sim()

    @staticmethod
    def run_multi_trade_simulation():
        RUN_multi_trade_sim()
