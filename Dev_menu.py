"""
The Dev_menu script is used to initiate all economic analysis, trading simulations,
and economic model parameters optimisations.
"""

# ============================ EVOLUTION-OPTIMISER =============================
from PhyTrade.ML_optimisation.EVOA_Optimisation.EVO_algo_2 import EVOA_optimiser
from PhyTrade.ML_optimisation.EVOA_Optimisation.Analysis_configs.Config_1 import Config_1

config = Config_1()

EVO_optimisation = EVOA_optimiser(config, run_label="Test_run")

# ============================ ECONOMIC ANALYSIS ===============================

from PhyTrade.Tools.EVAL_parameter_set import EVAL_parameter_set

# parameter_set =
