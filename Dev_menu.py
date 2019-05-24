"""
The Dev_menu script is used to initiate all economic analysis, trading simulations,
and economic model parameters evaluations and optimisations.
"""

# ============================ EVOLUTION-OPTIMISER =============================
from PhyTrade.Economic_model.Technical_Analysis.Data_Collection_preparation.Fetch_technical_data import fetch_technical_data

from PhyTrade.ML_optimisation.EVOA_Optimisation.EVO_algo_3 import EVOA_optimiser
from PhyTrade.ML_optimisation.EVOA_Optimisation.Analysis_configs.Config_0 import Config_0
from PhyTrade.ML_optimisation.EVOA_Optimisation.Analysis_configs.Config_1 import Config_1

config = Config_0()

for ticker in config.tickers:
    try:
        config.data_slice_start_index = -len(fetch_technical_data(ticker)) + config.data_slice_size
        EVO_optimisation = EVOA_optimiser(config, ticker)

    except:
        print("\n!!! Ticker ->", ticker, " <- invalid, moving to the next in the list !!!\n")
        continue

# ============================ ECONOMIC ANALYSIS ===============================
from PhyTrade.Tools.RUN_model import RUN_model
import json

# parameter_set = json.load(open(r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Run_3.json".replace('\\', '/')))
# evaluation = RUN_model("1", None, "INTC", -500, 450, 20)
