# ============================ DIRECT TRADERS ==================================
from PhyTrade.Trading_bots.Tradebot_v2 import Tradebot_v2

# Trader_1 = Tradebot_v1()
# Trader_2 = Tradebot_v2()
# Trader_3 = Tradebot_v3()

# dev_prototype()

# ============================ GENETICALY-OPTIMISED TRADING====================
from PhyTrade.GA_optimisation.GA_algo import GA_optimiser

GA_optimisation = GA_optimiser(population_size=20,
                               nb_of_generations=20,
                               mutation_rate=0.7,
                               nb_parents=5,
                               nb_random_ind=10)
