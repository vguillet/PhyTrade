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
import sys


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
                            max_worker_processes=1,
                            evaluation_setting=0,
                            calculate_stats=False, print_evaluation_status=False, plot_3=False):
        from PhyTrade.ML_optimisation.EVOA_optimisation.Tools.EVOA_benchmark_tool import Confusion_matrix_analysis

        metalabel_accuracies = []
        confusion_matrix_analysis = []
        net_worth = []

        # -- List based evaluation
        for i in range(len(population_lst)):

            population_lst[i].gen_economic_model(data_slice, plot_3=plot_3)
            population_lst[i].perform_trade_run(data_slice)

            if print_evaluation_status:
                print("\n ----------------------------------------------")
                print("Parameter set", i + 1, "evaluation completed:\n")
                print("Final net worth:", round(population_lst[i].account.net_worth_history[-1], 3), "$\n")

            individual_confusion_matrix_analysis = Confusion_matrix_analysis(population_lst[i].analysis.big_data.Major_spline.trade_signal,
                                                                             data_slice.metalabels,
                                                                             calculate_stats=calculate_stats,
                                                                             print_benchmark_results=print_evaluation_status)

            confusion_matrix_analysis.append(individual_confusion_matrix_analysis)
            metalabel_accuracies.append(individual_confusion_matrix_analysis.overall_accuracy_bs)
            net_worth.append(population_lst[i].account.net_worth_history[-1])

        # -- Multi-process evaluation
        # from PhyTrade.Tools.MULTI_PROCESSING_tools import multi_process_pool
        # def eval_function(individual):
        #     individual.gen_economic_model(data_slice_info, plot_3=plot_3)
        #
        #     return Confusion_matrix_analysis(individual.big_data.Major_spline.trade_signal,
        #                                      data_slice_info.metalabels.close_values_metalabels)
        #
        # accuracies_achieved = multi_process_pool(population_lst, eval_function, max_worker_processes=max_worker_processes)
        #
        # accuracies_achieved = MATH().normalise_zero_one(profit_achieved)

        if evaluation_setting == 0:
            fitness_evaluation = net_worth
        elif evaluation_setting == 1:
            fitness_evaluation = metalabel_accuracies

        return fitness_evaluation, metalabel_accuracies, confusion_matrix_analysis, net_worth

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
                            population_size, parents, nb_random_ind, mutation_rate=0.2):

        from PhyTrade.ML_optimisation.EVOA_optimisation.Tools.EVOA_random_gen import EVOA_random_gen
        from PhyTrade.Tools.INDIVIDUAL_gen import Individual
        import random
        from copy import deepcopy

        mutation_rate = EVOA_tools().throttle(current_generation, nb_of_generations, mutation_rate, 0.05, decay_function)
        nb_of_parameters_to_mutate = round(Individual().nb_of_parameters * mutation_rate)

        # --> Save single best parent to new population
        new_population = [parents[0]]

        # --> Generate offsprings from parents with mutations
        cycling = -1
        for _ in range(population_size - 1 - nb_random_ind):
            cycling += 1
            if cycling >= len(parents):
                cycling = 0

            offspring = deepcopy(parents[cycling])

            # --> Mutate offspring
            for _ in range(nb_of_parameters_to_mutate):
                parameter_type_to_modify = random.choice(list(offspring.parameter_dictionary.keys()))

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
                    if throttled_value >= min_value:
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
    def determine_evolving_gen_parameters(current_generation,
                                          data_slice_cycle_count):
        from SETTINGS import SETTINGS
        settings = SETTINGS()
        settings.gen_evoa_settings()
        # ------------------ Throttle the individual count to be used by the generation
        # --> Based on generation count
        nb_parents = round(EVOA_tools().throttle(current_generation,
                                                 settings.nb_of_generations-settings.exploitation_phase_len,
                                                 settings.nb_parents,
                                                 min_value=1,
                                                 decay_function=settings.parents_decay_function))
        # --> Based on cycle count
        nb_parents = round(EVOA_tools().throttle(data_slice_cycle_count,
                                                 settings.data_slice_cycle_count,
                                                 nb_parents,
                                                 min_value=1,
                                                 decay_function=settings.parents_decay_function))

        # --> Based on generation count
        nb_random_ind = round(EVOA_tools().throttle(current_generation,
                                                    settings.nb_of_generations-settings.exploitation_phase_len,
                                                    settings.nb_random_ind,
                                                    min_value=0,
                                                    decay_function=settings.random_ind_decay_function))
        # --> Based on cycle count
        nb_random_ind = round(EVOA_tools().throttle(data_slice_cycle_count,
                                                    settings.data_slice_cycle_count,
                                                    nb_random_ind,
                                                    min_value=0,
                                                    decay_function=settings.random_ind_decay_function))

        if settings.print_evoa_parameters_per_gen:
            print("~~~~~~~~~~~")
            print("Number of parents selected for this generation", nb_parents)
            print("Number of random individuals generated for this generation", nb_random_ind)
            print("~~~~~~~~~~~")

        return nb_parents, nb_random_ind
