from GAoptimisation.Individual_gen import Individual
from Trading_bots.Tradebot_v3 import Tradebot_v3
"""""
begin
    count = 0                                   \done
    initialize population                       \done
    evaluate population
    while not termination condition do
    begin
        count = count + 1
        select individuals for reproduction
        apply variation operators
        evaluate offspring
    end
end
"""""
# ========================= GA OPTIMISATION INITIALISATION =======================
population_size = 10

count = 0

# ~~~~~~~~~~~~~~~~~~ Initialise population
population_lst = []
for i in range(population_size):
    population_lst.append(Individual())

# ~~~~~~~~~~~~~~~~~~ Evaluate population

performance_lst = []
for parameter_set in population_lst:
    performance_lst.append(Tradebot_v3(parameter_set).account.net_worth_history[-1])

print(performance_lst)
