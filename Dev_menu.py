# ============================ DIRECT TRADERS ==================================

# Trader_1 = Tradebot_v1()
# Trader_2 = Tradebot_v2()
# Trader_3 = Tradebot_v3()

# dev_prototype()

# ============================ GENETICALY-OPTIMISED TRADING====================
from PhyTrade.GA_optimisation.GA_algo import GA_optimiser

GA_optimisation = GA_optimiser(population_size=5, nb_of_generations=10, mutation_rate=0.5)
