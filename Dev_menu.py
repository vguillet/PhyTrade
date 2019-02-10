# ============================ DIRECT TRADERS ==================================


# Trader_1 = Tradebot_v1()
# Trader_2 = Tradebot_v2()

# dev_prototype()

# ============================ GENETICALY-OPTIMISED TRADING ===================
# from PhyTrade.ML_optimisation.EVOA_Optimisation.EVO_algo import EVO_optimiser
#
#
# EVO_optimisation = EVO_optimiser(population_size=20,
#                                  nb_of_generations=60,
#
#                                  mutation_rate=0.5,
#                                  nb_parents=20,
#                                  nb_random_ind=20,
#
#                                  exploitation_phase_len=20,
#
#                                  data_slice_start_index=-7000,
#                                  data_slice_size=200,
#                                  data_slice_shift_per_gen=100)

# -------------------
from PhyTrade.ML_optimisation.EVOA_Optimisation.EVO_algo_2 import EVO_optimiser
from Analysis_configs.Config_1 import Config_1
from Analysis_configs.Config_0 import Config_0

config = Config_1()

EVO_optimisation = EVO_optimiser(config)