
##################################################################################################################
"""
This script contains the EVOA_tool class, used by the EVO_algo classes to perform EVOA optimisations
The class contains:
    - gen_initial_population()
    - evaluate_population()
    - select_from_population()
    - generate_offsprings()
    - throttle()
    - determine_evolving_gen_parameters()
"""

# Built-in/Generic Imports
import sys

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class EVOA_tools:
    @staticmethod
    def gen_initial_population(ticker, population_size=10):
        from PhyTrade.Tools.INDIVIDUAL_gen import Individual

        population_lst = []
        for i in range(population_size):
            population_lst.append(Individual(ticker=ticker))

        return population_lst

    @staticmethod
    def evaluate_population(population_lst, data_slice,
                            max_worker_processes=4,
                            evaluation_setting=0,
                            calculate_stats=False, multiprocessing=False,
                            print_evaluation_status=False, plot_eco_model_results=False):
        from PhyTrade.Signal_optimisation.EVO_algorithm.Tools.EVOA_benchmark_tool import Confusion_matrix_analysis
        from PhyTrade.Tools.Progress_bar_tool import Progress_bar

        confusion_matrix_analysis = []
        metalabel_accuracies = []
        metalabel_accuracies_bs = []
        avg_metalabel_accuracies = []
        net_worth = []
        buy_count = []
        sell_count = []
        transaction_count = []

        data_slice.perform_metatrade_run()
        metalabel_net_worth = data_slice.metalabels_account.net_worth_history[-1]

        # Disable progress bar and all print functions in case of multiprocessing run case
        if multiprocessing is False:
            progress_bar = Progress_bar(len(population_lst))

        # -- List based evaluation
        for i in range(len(population_lst)):
            if print_evaluation_status:
                print("\n--------------------------------------------------")
                print("Parameter set", i + 1)

            population_lst[i].gen_economic_model(data_slice, plot_eco_model_results=plot_eco_model_results)
            population_lst[i].perform_metatrade_run(data_slice)

            if print_evaluation_status:
                print("\nMetalabels net worth:", round(metalabel_net_worth), "$")
                print("Final net worth:", round(population_lst[i].account.net_worth_history[-1], 3), "$")
                print("\nTransaction count:", population_lst[i].tradebot.buy_count + population_lst[i].tradebot.sell_count)
                print("Buy count:", population_lst[i].tradebot.buy_count)
                print("Sell count:", population_lst[i].tradebot.sell_count, "\n")

            individual_confusion_matrix_analysis = Confusion_matrix_analysis(population_lst[i].trade_signal,
                                                                             data_slice.metalabels,
                                                                             calculate_stats=calculate_stats,
                                                                             print_benchmark_results=print_evaluation_status)

            # --> Save evaluations
            confusion_matrix_analysis.append(individual_confusion_matrix_analysis)

            # --> Save metalabel accuracies
            metalabel_accuracies.append(individual_confusion_matrix_analysis.overall_accuracy_bs)
            metalabel_accuracies_bs.append(individual_confusion_matrix_analysis.overall_accuracy)

            avg_metalabel_accuracies.append((individual_confusion_matrix_analysis.overall_accuracy+individual_confusion_matrix_analysis.overall_accuracy_bs)/2)

            # --> Save net worth
            net_worth.append(population_lst[i].account.net_worth_history[-1])
            buy_count.append(population_lst[i].tradebot.buy_count)
            sell_count.append(population_lst[i].tradebot.sell_count)
            transaction_count.append(population_lst[i].tradebot.buy_count + population_lst[i].tradebot.sell_count)

            if multiprocessing is False:
                progress_bar.update_progress()

        # -- Multi-thread evaluation
        # TODO: Add multithreading

        # --> Perform evaluation based on net worth
        if evaluation_setting == 0:
            fitness_evaluation = net_worth

        # --> Perform evaluation based on metalabels accuracies
        elif evaluation_setting == 1:
            fitness_evaluation = metalabel_accuracies

        # --> Perform evaluation based on metalabels buy/sell accuracies
        elif evaluation_setting == 2:
            fitness_evaluation = metalabel_accuracies_bs

        # --> Perform evaluation based on the average of net worth and metalabel accuracies
        elif evaluation_setting == 3:
            fitness_evaluation = avg_metalabel_accuracies

        elif evaluation_setting == 4:
            fitness_evaluation = buy_count

        elif evaluation_setting == 5:
            fitness_evaluation = sell_count

        elif evaluation_setting == 6:
            fitness_evaluation = transaction_count

        return fitness_evaluation, confusion_matrix_analysis, net_worth

    @staticmethod
    def select_from_population(fitness_evaluation, population, selection_method=0, nb_parents=3):
        if sum(fitness_evaluation) != 0:
            # --> Determine fitness ratio
            fitness_ratios = []
            for i in range(len(fitness_evaluation)):
                fitness_ratios.append(fitness_evaluation[i]/sum(fitness_evaluation)*100)

            # --> Select individuals
            parents = []

            # TODO: Implement alternative selection methods
            # --> Exit program if incorrect settings used
            if selection_method > 0:
                print("Invalid parent selection method reference")
                sys.exit()

            # Elitic selection
            if selection_method == 0:
                sorted_fitness_ratios = fitness_ratios
                sorted_population = population
                sorted_fitness_evaluation = fitness_evaluation

                # Use bubblesort to sort population, fitness_evaluation, and fitness_ratios according to fitness_ratio
                for _ in range(len(sorted_fitness_ratios)):
                    for i in range(len(sorted_fitness_ratios) - 1):
                        if sorted_fitness_ratios[i] < sorted_fitness_ratios[i + 1]:
                            sorted_fitness_ratios[i], sorted_fitness_ratios[i + 1] = sorted_fitness_ratios[i + 1], sorted_fitness_ratios[i]
                            sorted_population[i], sorted_population[i + 1] = sorted_population[i + 1], sorted_population[i]
                            sorted_fitness_evaluation[i], sorted_fitness_evaluation[i + 1] = sorted_fitness_evaluation[i + 1], sorted_fitness_evaluation[i]

                for i in range(nb_parents):
                    parents.append(sorted_population[i])

        else:
            # --> Select individuals randomly
            # TODO: Implement random selection
            parents = []
            for i in range(nb_parents):
                parents.append(population[i])

        return parents

    @staticmethod
    def generate_offsprings(ticker,
                            current_generation, nb_of_generations,
                            current_slice_cycle, nb_of_slice_cycles,
                            decay_function,
                            population_size, parents, nb_parents_in_next_gen, nb_random_ind,
                            parameter_blacklist=["general_settings"],
                            mutation_rate=0.2):

        from PhyTrade.Signal_optimisation.EVO_algorithm.Tools.EVOA_random_gen import EVOA_random_gen
        from PhyTrade.Tools.INDIVIDUAL_gen import Individual
        import random
        from copy import deepcopy

        nb_of_parameters_to_mutate = round(Individual().nb_of_parameters * mutation_rate) or 1

        # --> Save single best parent to new population
        new_population = parents[:nb_parents_in_next_gen]

        # --> Generate offsprings from parents with mutations
        cycling = -1
        for _ in range(population_size - nb_parents_in_next_gen - nb_random_ind):
            cycling += 1
            if cycling >= len(parents):
                cycling = 0

            offspring = deepcopy(parents[cycling])

            # --> Mutate offspring
            for _ in range(nb_of_parameters_to_mutate):
                # --> Select parameter class to modify
                parameter_class_to_modify = random.choice(list(offspring.parameter_set.keys()))
                while parameter_class_to_modify in parameter_blacklist:
                    parameter_class_to_modify = random.choice(list(offspring.parameter_set.keys()))

                # --> Select parameter type to modify
                parameter_type_to_modify = random.choice(list(offspring.parameter_set[parameter_class_to_modify].keys()))
                while parameter_type_to_modify in parameter_blacklist:
                    parameter_type_to_modify = random.choice(list(offspring.parameter_set[parameter_class_to_modify].keys()))

                offspring = EVOA_random_gen().modify_param(offspring, parameter_type_to_modify,
                                                           current_generation, nb_of_generations,
                                                           current_slice_cycle, nb_of_slice_cycles,
                                                           decay_function)

            new_population.append(offspring)

        # --> Create random_ind number of random individuals and add to new population
        for _ in range(nb_random_ind):
            new_population.append(Individual(ticker=ticker))

        return new_population

    @staticmethod
    def throttle(current_generation, nb_of_generations, max_value, min_value=1., decay_function=0):
        """
        Throttle a value according to the instance in the run time.

        The following decay functions settings can be used:
                0 - Fixed value (returns max value)

                1 - Linear decay

                2 - Logarithmic decay (in development)

        :param current_generation: Current generation
        :param nb_of_generations: Total number of generation in the run
        :param max_value: Max allowed value
        :param min_value: Min allowed value
        :param decay_function: Decay function setting
        :return: Throttled value
        """
        from math import log10
        # -- Exit program if incorrect settings used
        if decay_function > 2:
            print("Invalid throttle decay function reference")
            sys.exit()

        inverse = False
        if max_value < min_value:
            inverse = True

        # TODO: add decay functions (log/exponential etc...)
        if current_generation <= nb_of_generations:
            if decay_function == 0:       # Fixed value
                return max_value

            elif decay_function == 1:     # Linear decay
                if inverse:
                    throttled_value = max_value + (min_value-max_value)/nb_of_generations*current_generation
                    if throttled_value <= min_value:
                        throttled_value = min_value
                else:
                    throttled_value = max_value - (max_value-min_value)/nb_of_generations*current_generation
                    if throttled_value <= min_value:
                        throttled_value = min_value

            # TODO: Complete log decay
            elif decay_function == 2:       # Logarithmic decay
                throttled_value = max_value+log10(-(current_generation-nb_of_generations))

        else:
            throttled_value = min_value

        return throttled_value

    @staticmethod
    def determine_evolving_gen_parameters(settings, current_generation, data_slice_cycle_count):
        from PhyTrade.Tools.INDIVIDUAL_gen import Individual

        # ------------------ Throttle the individual count to be used by the generation
        # ---- Number of parents
        # --> Based on generation count
        nb_parents_gen = round(EVOA_tools().throttle(current_generation,
                                                     settings.nb_of_generations-settings.exploitation_phase_len,
                                                     settings.nb_parents,
                                                     min_value=1,
                                                     decay_function=settings.parents_decay_function))
        # --> Based on cycle count
        nb_parents_cycle = round(EVOA_tools().throttle(data_slice_cycle_count,
                                                       settings.data_slice_cycle_count,
                                                       settings.nb_parents,
                                                       min_value=1,
                                                       decay_function=settings.parents_decay_function))
        # --> Select smallest one
        nb_parents = min(nb_parents_gen, nb_parents_cycle)

        # ---- Number of parents included in next gen
        # --> Based on generation count
        nb_parents_in_next_gen_gen = round(EVOA_tools().throttle(current_generation,
                                                                 settings.nb_of_generations-settings.exploitation_phase_len,
                                                                 settings.nb_parents_in_next_gen,
                                                                 min_value=1,
                                                                 decay_function=settings.random_ind_decay_function))
        # --> Based on cycle count
        nb_parents_in_next_gen_cycle = round(EVOA_tools().throttle(data_slice_cycle_count,
                                                                   settings.data_slice_cycle_count,
                                                                   settings.nb_parents_in_next_gen,
                                                                   min_value=1,
                                                                   decay_function=settings.random_ind_decay_function))
        # --> Select smallest one
        nb_parents_in_next_gen = min(nb_parents_in_next_gen_gen, nb_parents_in_next_gen_cycle)

        # ---- Number of random individual
        # --> Based on generation count
        nb_random_ind_gen = round(EVOA_tools().throttle(current_generation,
                                                        settings.nb_of_generations-settings.exploitation_phase_len,
                                                        settings.nb_random_ind,
                                                        min_value=0,
                                                        decay_function=settings.random_ind_decay_function))
        # --> Based on cycle count
        nb_random_ind_cycle = round(EVOA_tools().throttle(data_slice_cycle_count,
                                                          settings.data_slice_cycle_count,
                                                          settings.nb_random_ind,
                                                          min_value=0,
                                                          decay_function=settings.random_ind_decay_function))
        # --> Select smallest one
        nb_random_ind = min(nb_random_ind_gen, nb_random_ind_cycle)

        # ---- Mutation rate
        # --> Based on generation count
        mutation_rate_gen = EVOA_tools().throttle(current_generation,
                                                  settings.nb_of_generations-settings.exploitation_phase_len,
                                                  settings.mutation_rate,
                                                  min_value=0.1,
                                                  decay_function=settings.random_ind_decay_function)
        # --> Based on cycle count
        mutation_rate_cycle = EVOA_tools().throttle(data_slice_cycle_count,
                                                    settings.data_slice_cycle_count,
                                                    settings.mutation_rate,
                                                    min_value=0.1,
                                                    decay_function=settings.random_ind_decay_function)
        # --> Select smallest one
        mutation_rate = min(mutation_rate_gen, mutation_rate_cycle)

        if settings.print_evoa_parameters_per_gen:
            print("Number of parents selected:", nb_parents)
            print("Number of parents included:", nb_parents_in_next_gen)
            print("Number of random individuals included:", nb_random_ind)
            print("Number of parameters mutated:",
                  str(round(Individual().nb_of_parameters*mutation_rate) or 1)+"/"+str(Individual().nb_of_parameters), "\n")

        return nb_parents, nb_parents_in_next_gen, nb_random_ind, mutation_rate
