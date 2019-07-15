"""
The Dev_menu script is used to initiate all economic analysis, trading simulations,
and economic model parameters evaluations and optimisations.
"""
from PhyTrade.Settings.SETTINGS import SETTINGS

from PhyTrade.Signal_optimisation.EVOA_optimisation.EVO_algo_4 import EVOA_optimiser
from PhyTrade.Economic_model.RUN_model import RUN_model
from PhyTrade.Trade_simulations.RUN_single_trade_sim import RUN_single_trade_sim
from PhyTrade.Trade_simulations.RUN_multi_trade_sim import RUN_multi_trade_sim
from PhyTrade.Backtesting.Metalabeling.EVOA_METALABELS_gen import gen_ticker_metalabels

print("-- Welcome to the PhyTrade Economic analyser and modeling tool --")
print("Select the wanted run process:")
print("1 - RUN EVOA Optimiser")
print("2 - GEN EVOA Metalabels")
print("3 - RUN Model")
print("4 - RUN Single ticker trading simulation")
print("5 - RUN Multi ticker trading simulation (in development)")
print("")
print("0 - Exit")

run = True
while run is True:
    selection = int(input("Enter selection:\n"))
    # selection = 1
    settings = SETTINGS()
    print("\n")

    # ============================ EVOLUTION-OPTIMISER =============================
    if selection == 1:
        # --> Generate market settings
        settings.market_settings.gen_market_settings()

        def optimise(settings, ticker):
            try:
                # settings.data_slice_start_index = -len(fetch_technical_data(ticker)) + settings.data_slice_size
                EVOA_optimiser(settings, ticker, optimiser_setting=1)
            except:
                print("\n!!! Ticker ->", ticker, " <- invalid, moving to the next in the list !!!\n")

        # for ticker in settings.market_settings.tickers:
        #     optimise(settings, ticker)

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
