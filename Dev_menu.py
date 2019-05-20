"""
The Dev_menu script is used to initiate all economic analysis, trading simulations,
and economic model parameters optimisations.
"""

# ============================ EVOLUTION-OPTIMISER =============================
from PhyTrade.ML_optimisation.EVOA_Optimisation.EVO_algo_3 import EVOA_optimiser
from PhyTrade.ML_optimisation.EVOA_Optimisation.Analysis_configs.Config_0 import Config_0
from PhyTrade.ML_optimisation.EVOA_Optimisation.Analysis_configs.Config_1 import Config_1


# config = Config_0()
# EVO_optimisation = EVOA_optimiser(config)

# ============================ ECONOMIC ANALYSIS ===============================
from PhyTrade.Tools.RUN_model import RUN_model
import json

parameter_set = json.load(open(r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Run_3.json".replace('\\', '/')))
evaluation = RUN_model("1", None, "AAPL", -500, 450, 20)
