from GAoptimisation.POPULATION_gen import Population
"""""
begin
    count = 0
    initialize population
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

for i in range(population_size)
population = Population()

