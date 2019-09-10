
##################################################################################################################
"""
The Dev_menu script is used to initiate all economic analysis, trading simulations,
and economic model parameters evaluations and optimisations.
"""

# Own modules
from PhyTrade.Settings.SETTINGS import SETTINGS
from PhyTrade.Data_Collection_preparation.Fetch_parameter_set_labels_df import fetch_parameter_set_labels_df
from PhyTrade.Tools.Colours_and_Fonts import cf

from PhyTrade.Signal_optimisation.EVOA_optimisation.EVO_algo_4 import EVOA_optimiser
from PhyTrade.Economic_model.RUN_model import RUN_model
from PhyTrade.Trade_simulations.RUN_single_trade_sim import RUN_single_trade_sim
from PhyTrade.Trade_simulations.RUN_multi_trade_sim import RUN_multi_trade_sim
from PhyTrade.Backtesting.Metalabeling.EVOA_METALABELS_gen import gen_ticker_metalabels

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################

print(cf["bold"] + cf["cyan"] + "\n-- Welcome to the PhyTrade Economic analyser and modeling tool --" + cf["reset"])
print("\nSelect the wanted run process:")
print(cf["bold"] + "\n> == Model training and optimisation == <" + cf["reset"])
print(cf["green"] + "1 - RUN EVOA Optimiser" + cf["reset"])
print(cf["green"] + "2 - GEN EVOA Metalabels" + cf["reset"])

print(cf["bold"] + "\n> == Model and parameter evaluation == <" + cf["reset"])
print(cf["green"] + "3 - RUN Model" + cf["reset"])

print(cf["bold"] + "\n> == Trading simulations == <" + cf["reset"])

print(cf["green"] + "4 - RUN Single ticker trading simulation" + cf["reset"])
print(cf["green"] + "5 - RUN Multi ticker trading simulation" + cf["reset"])

print("\n-------------------------------------------------------------------------")
print("Parameter sets available:")
fetch_parameter_set_labels_df()

print("\n" + cf["red"] + "0 - Exit" + cf["reset"])

run = True
while run is True:
    selection = int(input("\nSelection:\n"))
    # selection = 1
    settings = SETTINGS()
    print("\n")

    # ============================ EVOLUTION-OPTIMISER =============================
    if selection == 1:
        # --> Generate market settings
        settings.market_settings.gen_market_settings()

        def optimise(settings, ticker):
            try:
                settings.fetch_dates(1)
                EVOA_optimiser(settings, ticker, optimiser_setting=1)
            except:
                print("\n!!! Ticker ->", ticker, " <- invalid, moving to the next in the list !!!\n")

        # for ticker in settings.market_settings.tickers:
        #     optimise(settings, ticker)

        settings.fetch_dates(1)
        EVOA_optimiser(settings, settings.market_settings.tickers[0], optimiser_setting=1)

    # ============================ EVOLUTION-METALABELING ==========================

    if selection == 2:
        # --> Generate market settings
        settings.market_settings.gen_market_settings()

        for ticker in settings.market_settings.tickers:
            gen_ticker_metalabels(settings, ticker)

    # ============================ ECONOMIC ANALYSIS ===============================
    elif selection == 3:
        run_model = RUN_model()

    # ============================ TRADING SIMULATIONS ==============================
    elif selection == 4:
        run_trade_sim = RUN_single_trade_sim()

    elif selection == 5:
        run_trade_sim = RUN_multi_trade_sim()

    elif selection == 0:
        import sys
        sys.exit()

    else:
        print("Invalid selection")
