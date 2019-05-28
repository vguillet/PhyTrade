"""
The Dev_menu script is used to initiate all economic analysis, trading simulations,
and economic model parameters evaluations and optimisations.
"""

# ============================ EVOLUTION-OPTIMISER =============================
from PhyTrade.ML_optimisation.EVOA_Optimisation.Analysis_configs.Config_0 import Config_0
from PhyTrade.ML_optimisation.EVOA_Optimisation.Analysis_configs.Config_1 import Config_1
from PhyTrade.ML_optimisation.EVOA_Optimisation.EVO_algo_3 import EVOA_optimiser
from PhyTrade.Economic_model.Technical_Analysis.Data_Collection_preparation.Fetch_technical_data import fetch_technical_data

# config = Config_0()
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
evaluation = RUN_trade_sim("1", parameter_set, "AAPL", "2000-01-01", 200, 15,
                           plot_signal=False, print_trade_process=False)
