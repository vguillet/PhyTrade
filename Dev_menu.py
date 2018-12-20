# ============================ DIRECT TRADERS ==================================
from PhyTrade.Trading_bots.Tradebot_v1 import Tradebot_v1
from PhyTrade.Trading_bots.Tradebot_v2 import Tradebot_v2
from PhyTrade.Trading_bots.Tradebot_v3 import Tradebot_v3

from PhyTrade.Tools.DATA_SLICE_gen import data_slice_info

data_slice_info = data_slice_info(-400, -200, 50)

# Trader_1 = Tradebot_v1()
# Trader_2 = Tradebot_v2()

# dev_prototype()

# ============================ GENETICALY-OPTIMISED TRADING ===================
from PhyTrade.GA_optimisation.GA_algo import GA_optimiser

GA_optimisation = GA_optimiser(population_size=20,
                               nb_of_generations=20,

                               mutation_rate=0.4,
                               nb_parents=10,
                               nb_random_ind=5,

                               exploitation_phase_len=5,

                               data_slice_start_index=-3000,
                               data_slice_size=200,
                               data_slice_shift_per_gen=50)
