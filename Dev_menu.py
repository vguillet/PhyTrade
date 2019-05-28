"""
The Dev_menu script is used to initiate all economic analysis, trading simulations,
and economic model parameters evaluations and optimisations.
"""

# ============================ EVOLUTION-OPTIMISER =============================

# config = Config_1()
#
# for ticker in config.tickers:
#     try:
#         config.data_slice_start_index = -len(fetch_technical_data(ticker)) + config.data_slice_size
#         EVO_optimisation = EVOA_optimiser(config, ticker)
#
#     except:
#         print("\n!!! Ticker ->", ticker, " <- invalid, moving to the next in the list !!!\n")
#         continue

# ============================ ECONOMIC ANALYSIS ===============================
from PhyTrade.RUN_trade_sim import RUN_trade_sim
import json

parameter_set = json.load(open(r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Parameter_sets\Run_2_AAPL.json".replace('\\', '/')))
evaluation = RUN_trade_sim("1", parameter_set, "AAPL", -7001, 200, 35,
                           plot_signal=False, print_trade_process=False)
