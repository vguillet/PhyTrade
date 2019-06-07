"""
The Dev_menu script is used to initiate all economic analysis, trading simulations,
and economic model parameters evaluations and optimisations.
"""
from SETTINGS import SETTINGS
from PhyTrade.ML_optimisation.EVOA_Optimisation.EVO_algo_3 import EVOA_optimiser
from PhyTrade.Economic_model.RUN_model import RUN_model
from PhyTrade.Trade_simulations.RUN_single_trade_sim import RUN_single_trade_sim
from PhyTrade.Trade_simulations.RUN_multi_trade_sim import RUN_multi_trade_sim

from PhyTrade.Economic_model.Technical_Analysis.Data_Collection_preparation.Fetch_technical_data import fetch_technical_data


print("-- Welcome to the PhyTrade Economic analyser and modeling tool --")
print("Select the wanted run process:")
print("1 - RUN EVOA Optimiser")
print("2 - RUN Model")
print("3 - RUN Single ticker trading simulation")
print("4 - RUN Multi ticker trading simulation (in development)")
print("")
print("0 - Exit")

run = True
while run is True:
    settings = SETTINGS()

    selection = int(input("Enter selection:\n"))
    # ============================ EVOLUTION-OPTIMISER =============================
    if selection == 1:

        # --> Generate evoa settings
        settings.gen_evoa_settings()

        ticker = settings.tickers[0]
        # for ticker in config.tickers:
        #     try:
        settings.data_slice_start_index = -len(fetch_technical_data(ticker)) + settings.data_slice_size
        EVO_optimisation = EVOA_optimiser(ticker)

        # except:
        #     print("\n!!! Ticker ->", ticker, " <- invalid, moving to the next in the list !!!\n")
        #     continue

    # ============================ ECONOMIC ANALYSIS ===============================
    elif selection == 2:
        run_model = RUN_model()

    # ============================ TRADING SIMULATIONS ==============================
    elif selection == 3:
        run_trade_sim = RUN_single_trade_sim()

    elif selection == 4:
        run_trade_sim = RUN_multi_trade_sim()

    elif selection == 0:
        import sys
        sys.exit()

    else:
        print("Invalid selection")
