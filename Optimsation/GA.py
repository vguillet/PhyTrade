# import random
#
# #
# # Global variables
# # Setup optimal string and GA input variables.
# #
#
# OPTIMAL     = 0                 # Ideal settle time is zero
# DNA_SIZE    = 6                      # Amount of columns in parameter text file ??
# POP_SIZE    = 20
# GENERATIONS = 30
#
# with open('../ResultingSettleTimes.txt') as f:
#     items = f.readlines()
# # you may also want to remove whitespace characters like `\n` at the end of each line
# items = [x.strip('\n') for x in items]
#
# #
# # Helper functions
# # These are used as support, but aren't direct GA-specific functions.
# #
# def random_Aff():
#     """
#     Return a random value of Aff between 0 and 6000.
#     """
#     return int(random.randrange(0, 6000, 1))
#
# def random_Vff():
#     """
#     Return a random value of Vff between 0 and 40.
#     """
#     return float(40*random.uniform(0,1))
#
# def random_RampRate():
#     """
#     Return a random value of Ramp Rate between 0 and 10000.
#     """
#     return int(random.randrange(0, 10000, 1))
#
# def random_TrajFIRFilter():
#     """
#     Return a random value of Aff between 0 and 6000.
#     """
#     return int(random.randrange(0, 10, 1))
#
# def random_FFA():
#     """
#     Return a random value of Feedforward Advance between 0 and 1.
#     """
#     return float(random.randrange(0, 8, 1)/8)
#
# def random_population():
#     """
#     Return a list of POP_SIZE individuals, each randomly generated via iterating
#     DNA_SIZE times to generate a string of random characters with random_char().
#     """
#     pop = []
#     for i in xrange(POP_SIZE):
#         #dna = ""
#         dna_Aff = 0
#         dna_Vff = 0
#         dna_RampRate = 0
#         dna_TrajFIRFilter = 0
#         dna_FFA = 0
#         for c in xrange(DNA_SIZE):
#             #dna += random_char()
#             #pop.append(dna)
#             dna_Aff += random_Aff()
#             dna_Vff += random_Vff()
#             dna_FFA += random_FFA()
#             dna_TrajFIRFilter += random_TrajFIRFilter()
#             dna_RampRate += random_RampRate()
#             pop.append(dna_Aff, dna_Vff. dna_FFA, dna_TrajFIRFilter, dna_RampRate)
#     return pop
#
# def weighted_choice(items):
#     """
#     Chooses a random element from items, where items is a list of tuples in
#     the form  (GainAff, GainVff, FFA, TrajFIR, Ramp Rate, Settle Time).
#     weight determines the probability of choosing its respective item.
#     """
#     weight_total = sum((item[5] for item in items)) #Weighting is Settle Time (6th column)
#     n = random.uniform(0, weight_total)
#     for item, weight in items:                  #This is if there are arrays with 1 thing and 1 weight - we have 5 things
#         if n < weight:
#             return item
#         n = n - weight
#     return item
#
#
# #
# # GA functions
# # These make up the bulk of the actual GA algorithm.
# #
#
# def fitness(dna):
#     """
#     For each settle time in 'ResultingSettleTime.txt', this function calculates the difference between
#     it and the OPTIMAL value, which is zero in this case. Here, LOWER fitness value is better.
#     """
#     fitness = 0
#     fitness += items[5]
#     return fitness
#
# def mutate(dna):
#     """
#     For each gene in the DNA, there is a 1/mutation_chance chance that it will be
#     switched out with a random value. This ensures diversity in the
#     population, and ensures that is difficult to get stuck in local minima.
#     """
#     for i in range(0,len(items)):
#         mutation_chance = 100
#         if int(random.random()*mutation_chance) == 1:
#             if i == 0:
#                 dna_Aff += random_Aff()
#             if i == 1:
#                 dna_Vff += random_Vff()
#             if i == 2:
#                 dna_RampRate += random_RampRate()
#             if i == 3:
#                 dna_TrajFIRFilter += random_TrajFIRFilter()
#             if i == 4:
#                 dna_FFA += random_FFA()
#
# #def crossover(dna1, dna2):
# #  """
# #  Slices both dna1 and dna2 into two parts at a random index within their
# #  length and merges them. Both keep their initial sublist up to the crossover
# #  index, but their ends are swapped.
# #  """
# #  pos = int(random.random()*DNA_SIZE)
# #  return (dna1[:pos]+dna2[pos:], dna2[:pos]+dna1[pos:])
#
# #
# # Main driver
# # Generate a population and simulate GENERATIONS generations.
# #
#
# if __name__ == "__main__":
#   # Generate initial population. This will create a list of POP_SIZE strings,
#   # each initialized to a sequence of random characters.
#   population = random_population()
#
#   # Simulate all of the generations.
#   for generation in xrange(GENERATIONS):
#     print "Generation %s... Random sample: '%s'" % (generation, population[0])
#     weighted_population = []
#
#     # Add individuals and their respective fitness levels to the weighted
#     # population list. This will be used to pull out individuals via certain
#     # probabilities during the selection phase. Then, reset the population list
#     # so we can repopulate it after selection.
#     for individual in population:
#       fitness_val = fitness(individual)
#
#       # Generate the (individual,fitness) pair, taking in account whether or
#       # not we will accidently divide by zero.
#       if fitness_val == 0:
#         pair = (individual, 1.0)
#       else:
#         pair = (individual, 1.0/fitness_val)
#
#       weighted_population.append(pair)
#
#     population = []
#
#     # Select two random individuals, based on their fitness probabilites, cross
#     # their genes over at a random point, mutate them, and add them back to the
#     # population for the next iteration.
#     for _ in xrange(POP_SIZE/2):
#       # Selection
#       ind1 = weighted_choice(weighted_population)
#       ind2 = weighted_choice(weighted_population)
#
#       # Crossover
#       #ind1, ind2 = crossover(ind1, ind2)
#
#       # Mutate and add back into the population.
#       population.append(mutate(ind1))
#       population.append(mutate(ind2))
#
#   # Display the highest-ranked string after all generations have been iterated
#   # over. This will be the closest string to the OPTIMAL string, meaning it
#   # will have the smallest fitness value. Finally, exit the program.
#   #fittest_string = population[0]
#   #minimum_fitness = fitness(population[0])
#
#   #for individual in population:
#   #  ind_fitness = fitness(individual)
#   #  if ind_fitness <= minimum_fitness:
#   #    fittest_string = individual
#   #    minimum_fitness = ind_fitness
#
#   #print "Fittest String: %s" % fittest_string
#   exit(0)