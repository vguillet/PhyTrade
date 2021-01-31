
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
import random
from copy import deepcopy

# Own modules
from PhyTrade.Signal_optimisation.EVO_algorithm.Tools.EVOA_benchmark_tool import Confusion_matrix_analysis
from PhyTrade.Signal_optimisation.EVO_algorithm.Tools.EVOA_parameter_randomiser_tool import EVOA_parameter_randomiser
from PhyTrade.Signal_optimisation.EVO_algorithm.Tools.Throttle_tool import throttle
from PhyTrade.Building_blocks.Individual import Individual
from PhyTrade.Tools.Progress_bar_tool import Progress_bar

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class EVOA_tools:
    @staticmethod
    def gen_initial_population(population_size=10):
        """
        Used to generate an initial population of Individuals with random parameter sets of a given length

        :param population_size: Size of desired population
        :return: List of individuals of length population_size
        """

        population_lst = []
        for i in range(population_size):
            population_lst.append(Individual())

        return population_lst

    @staticmethod
    def evaluate_population(population_lst, data_slice,
                            max_worker_processes=4,
                            evaluation_setting=0,
                            calculate_stats=False, multiprocessing=False,
                            print_evaluation_status=False, plot_eco_model_results=False):
        """
        Used to evaluate a population (the trading performance of every individuals over a given subslice).
        Multiple evaluation methods are available, and evaluate the trading performance based on different metrics.

        They can be selected using the following setting:
            0 - Net worth
            1 - Metalabel accuracies
            2 - Metalabel buy/sell accuracy
            3 - Average of net worth and metalabel accuracies (1:1)
            4 - Number of buy signals generated
            5 - Number of sell signals generated
            6 - Number of transaction signals generated

        Three things returned:
            - List of the evaluation of each individual (according to provided evaluation setting)
              in provided population list (in the same order)
            - List of confusion_matrix_analysis objects (in the same order)
            - List of net worth of each individual (in the same order)

        :param population_lst: List of individuals to evaluate
        :param data_slice: Data_slice object to use for evaluation
        :param max_worker_processes: Number of worker processes to spawn (Not functional yet)
        :param evaluation_setting: Evaluation method to use (1 - 6)
        :param calculate_stats: Boolean
        :param multiprocessing: Boolean
        :param print_evaluation_status: Boolean
        :param plot_eco_model_results: Boolean
        :return: fitness_evaluation (list) (according to evaluation settting),
                 confusion_matrix_analysis (list of confusion_matrix_analysis (obj)),
                 net_worth (list)
        """
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

            population_lst[i].gen_economic_model(data_slice=data_slice,
                                                 plot_eco_model_results=plot_eco_model_results)

            population_lst[i].perform_trade_run(data_slice=data_slice)

            if print_evaluation_status:
                print("\nMetalabels net worth:", round(metalabel_net_worth), "$")
                print("Final net worth:", round(population_lst[i].account.net_worth_history[-1], 3), "$")
                print("\nTransaction count:", population_lst[i].tradebot.buy_count + population_lst[i].tradebot.sell_count)
                print("Buy count:", population_lst[i].tradebot.buy_count)
                print("Sell count:", population_lst[i].tradebot.sell_count, "\n")

            individual_confusion_matrix_analysis = Confusion_matrix_analysis(model_predictions=population_lst[i].analysis.trade_signal,
                                                                             metalabels=data_slice.metalabels,
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

        # --> Perform evaluation based on the number of buy signals generated
        elif evaluation_setting == 4:
            fitness_evaluation = buy_count

        # --> Perform evaluation based on the number of sell signals generated
        elif evaluation_setting == 5:
            fitness_evaluation = sell_count

        # --> Perform evaluation based on the number of transactions signals generated
        elif evaluation_setting == 6:
            fitness_evaluation = transaction_count

        else:
            sys.exit("No fitness evaluation method selected")

        # TODO: Rethink net worth?
        return fitness_evaluation, confusion_matrix_analysis, net_worth

    @staticmethod
    def select_from_population(fitness_evaluation, population, selection_method=0, nb_parents=3):
        """
        Used to select individuals from a generation to be used in the next one.
        Multiple selection methods are available, including:
            0 - Elitic selection
            1 - To be added

        A list of selected individual (obj) is returned.

        :param fitness_evaluation: List
        :param population: List of individuals obj
        :param selection_method: Selection method setting (0-Elitic)
        :param nb_parents: Nb of desired individuals obj to be selected
        :return: List of selected individual (obj)
        """

        if sum(fitness_evaluation) != 0:
            # --> Determine fitness ratio
            fitness_ratios = []
            for i in range(len(fitness_evaluation)):
                fitness_ratios.append(fitness_evaluation[i]/sum(fitness_evaluation)*100)

            # --> Select individuals
            parents = []

            # TODO: Implement alternative selection methods
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

            # --> Exit program if incorrect settings used
            else:
                sys.exit("Invalid parent selection method reference")

        else:
            # --> Select individuals randomly
            # TODO: Implement random selection
            parents = []
            for i in range(nb_parents):
                parents.append(population[i])

        return parents

    @staticmethod
    def generate_offsprings(current_generation, nb_of_generations,
                            current_subslice_cycle, nb_of_subslice_cycles,
                            decay_function,
                            population_size, parents, nb_parents_in_next_gen, nb_random_ind,
                            parameter_blacklist=["general_settings"],
                            mutation_rate=0.2):
        """
        Used to generate offsprings from parents with parameter variations.
        An offspring is generated form every parent sequentially until the required number of offsprings
        has been generated. The amount of variation present in the offsprings can be adjusted to gradually evolve,
        and be set according to the level of progress in an evolutionary process, and the decay function desired.

        :param current_generation: Current generation number
        :param nb_of_generations: Total generations count
        :param current_subslice_cycle: Current subslice cycle number
        :param nb_of_subslice_cycles: Total subslice cycle count
        :param decay_function: Desired decay function (0-Fixed value, 1-Linear decay, 2-Logarithmic decay (in development))
        :param population_size: Total required size of new population
        :param parents: List of individual obj
        :param nb_parents_in_next_gen: Number of parents to include in new population
        :param nb_random_ind: Number of random individuals to include in new population
        :param parameter_blacklist: Parameters to not modify from parents
        :param mutation_rate: Fraction of parameters to mutate
        :return: List of individual obj (new population)
        """

        # TODO: Throttle number of parameters to mutate
        nb_of_parameters_to_mutate = round(Individual().nb_of_parameters * mutation_rate) or 1

        # --> Add required number of parents to new population (from best to worst)
        new_population = parents[:nb_parents_in_next_gen]

        # --> Generate offsprings from parents with mutations
        cycling = -1
        for _ in range(population_size - nb_parents_in_next_gen - nb_random_ind):
            cycling += 1
            if cycling >= len(parents):
                cycling = 0

            offspring = deepcopy(parents[cycling])

            # --> Mutate offspring

            parameter_randomiser = EVOA_parameter_randomiser()  # Initiate parameter randomiser

            for _ in range(nb_of_parameters_to_mutate):
                # --> Select parameter class to modify
                parameter_class_to_modify = random.choice(list(offspring.parameter_set.keys()))
                while parameter_class_to_modify in parameter_blacklist:
                    parameter_class_to_modify = random.choice(list(offspring.parameter_set.keys()))

                # --> Select parameter type to modify
                parameter_type_to_modify = random.choice(list(offspring.parameter_set[parameter_class_to_modify].keys()))
                while parameter_type_to_modify in parameter_blacklist:
                    parameter_type_to_modify = random.choice(list(offspring.parameter_set[parameter_class_to_modify].keys()))

                offspring = parameter_randomiser.modify_param(offspring=offspring,
                                                              parameter_type_to_modify=parameter_type_to_modify,
                                                              current_generation=current_generation,
                                                              nb_of_generations=nb_of_generations,
                                                              current_subslice_cycle=current_subslice_cycle,
                                                              nb_of_subslice_cycles=nb_of_subslice_cycles,
                                                              decay_function=decay_function)

            new_population.append(offspring)

        # --> Create random_ind number of random individuals and add to new population
        for _ in range(nb_random_ind):
            new_population.append(Individual())

        return new_population

    @staticmethod
    def determine_evolving_gen_parameters(settings, current_generation, subslice_cycle_count):
        """
        Used to adjust generation parameters, including:
            - Number of parents
            - Number of parents included in next gen
            - Number of random individual
            - Mutation rate

        The parameters are adjusted every time according to the generation progress and cycle progress separately,
        the smallest value is retained
        # TODO: Review whether to combine or use min of throttled parameters results

        :param settings: Settings object
        :param current_generation: Current generation number
        :param subslice_cycle_count: Current cycle number
        :return: nb_parents, nb_parents_in_next_gen, nb_random_ind, mutation_rate
        """
        # ------------------ Throttle the individual count to be used by the generation
        # ---- Number of parents
        # --> Based on generation count
        nb_parents_gen = round(throttle(current_iteration=current_generation,
                                        nb_of_iterations=settings.nb_of_generations - settings.exploitation_phase_len,
                                        max_value=settings.nb_parents,
                                        min_value=1,
                                        decay_function=settings.parents_decay_function))
        # --> Based on cycle count
        nb_parents_cycle = round(throttle(current_iteration=subslice_cycle_count,
                                          nb_of_iterations=settings.subslice_cycle_count,
                                          max_value=settings.nb_parents,
                                          min_value=1,
                                          decay_function=settings.parents_decay_function))
        # --> Select smallest one
        nb_parents = min(nb_parents_gen, nb_parents_cycle)

        # ---- Number of parents included in next gen
        # --> Based on generation count
        nb_parents_in_next_gen_gen = round(throttle(current_iteration=current_generation,
                                                    nb_of_iterations=settings.nb_of_generations-settings.exploitation_phase_len,
                                                    max_value=settings.nb_parents_in_next_gen,
                                                    min_value=1,
                                                    decay_function=settings.random_ind_decay_function))
        # --> Based on cycle count
        nb_parents_in_next_gen_cycle = round(throttle(current_iteration=subslice_cycle_count,
                                                      nb_of_iterations=settings.subslice_cycle_count,
                                                      max_value=settings.nb_parents_in_next_gen,
                                                      min_value=1,
                                                      decay_function=settings.random_ind_decay_function))
        # --> Select smallest one
        nb_parents_in_next_gen = min(nb_parents_in_next_gen_gen, nb_parents_in_next_gen_cycle)

        # ---- Number of random individual
        # --> Based on generation count
        nb_random_ind_gen = round(throttle(current_iteration=current_generation,
                                           nb_of_iterations=settings.nb_of_generations-settings.exploitation_phase_len,
                                           max_value=settings.nb_random_ind,
                                           min_value=0,
                                           decay_function=settings.random_ind_decay_function))
        # --> Based on cycle count
        nb_random_ind_cycle = round(throttle(current_iteration=subslice_cycle_count,
                                             nb_of_iterations=settings.subslice_cycle_count,
                                             max_value=settings.nb_random_ind,
                                             min_value=0,
                                             decay_function=settings.random_ind_decay_function))
        # --> Select smallest one
        nb_random_ind = min(nb_random_ind_gen, nb_random_ind_cycle)

        # ---- Mutation rate
        # --> Based on generation count
        mutation_rate_gen = throttle(current_iteration=current_generation,
                                     nb_of_iterations=settings.nb_of_generations-settings.exploitation_phase_len,
                                     max_value=settings.mutation_rate,
                                     min_value=0.1,
                                     decay_function=settings.random_ind_decay_function)
        # --> Based on cycle count
        mutation_rate_cycle = throttle(current_iteration=subslice_cycle_count,
                                       nb_of_iterations=settings.subslice_cycle_count,
                                       max_value=settings.mutation_rate,
                                       min_value=0.1,
                                       decay_function=settings.random_ind_decay_function)
        # --> Select smallest one
        mutation_rate = min(mutation_rate_gen, mutation_rate_cycle)

        if settings.print_evoa_parameters_per_gen:
            print("Number of parents selected:", nb_parents)
            print("Number of parents included:", nb_parents_in_next_gen)
            print("Number of random individuals included:", nb_random_ind)
            print("Number of parameters mutated:",
                  str(round(Individual().nb_of_parameters*mutation_rate) or 1)+"/"+str(Individual().nb_of_parameters),
                  "\n")

        return nb_parents, nb_parents_in_next_gen, nb_random_ind, mutation_rate
