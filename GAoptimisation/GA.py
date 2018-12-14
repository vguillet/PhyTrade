from GAoptimisation.Individual_gen import Individual
from Trading_bots.Tradebot_v3 import Tradebot_v3
"""""
begin
    count = 0                                   \done
    initialize population                       \done
    evaluate population                         \done
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
for i in range(len(population_lst)):
    performance_lst.append(Tradebot_v3(population_lst[i]).account.net_worth_history[-1])
    print("Parameter set ", i+1, "evaluation completed")


print(performance_lst)
print(max(performance_lst))
