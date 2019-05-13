"""
The Dev_menu script is used to initiate all economic analysis, trading simulations,
and economic model parameters optimisations.
"""

# ============================ EVOLUTION-OPTIMISER =============================
from PhyTrade.ML_optimisation.EVOA_Optimisation.EVO_algo_3 import EVOA_optimiser
from PhyTrade.ML_optimisation.EVOA_Optimisation.Analysis_configs.Config_0 import Config_0
from PhyTrade.ML_optimisation.EVOA_Optimisation.Analysis_configs.Config_1 import Config_1


# config = Config_1()
# EVO_optimisation = EVOA_optimiser(config)

# ============================ ECONOMIC ANALYSIS ===============================
from PhyTrade.Tools.EVAL_parameter_set import EVAL_parameter_set
import json

parameter_set = json.load(open(r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Run 1.json".replace('\\', '/')))

evaluation = EVAL_parameter_set("1", parameter_set, "AAPL", -500, 450, 20)
