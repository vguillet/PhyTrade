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
    def gen_initial_population(population_size=10):
        from PhyTrade.ML_optimisation.EVOA_Optimisation.INDIVIDUAL_gen import Individual

        population_lst = []
        for i in range(population_size):
            population_lst.append(Individual())

        return population_lst

    @staticmethod
    def evaluate_population(population_lst, data_slice_info,
                            max_worker_processes=1,
                            calculate_stats=False, print_evaluation_status=False, plot_3=False):
        from PhyTrade.ML_optimisation.EVOA_Optimisation.EVOA_tools.EVOA_benchmark_tool import Confusion_matrix_analysis

        metalabel_accuracies = []
        confusion_matrix_analysis = []
        net_worth = []

        # -- List based evaluation
        for i in range(len(population_lst)):

            population_lst[i].gen_economic_model(data_slice_info, plot_3=plot_3)
            population_lst[i].perform_trade_run()

            if print_evaluation_status:
                print("\n ----------------------------------------------")
                print("Parameter set", i + 1, "evaluation completed:\n")
                print("Final net worth:", round(population_lst[i].account.net_worth_history[-1], 3), "$\n")

            individual_confusion_matrix_analysis = Confusion_matrix_analysis(population_lst[i].analysis.big_data.Major_spline.trade_signal,
                                                                             data_slice_info.metalabels.close_values_metalabels,
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

        return metalabel_accuracies, confusion_matrix_analysis, net_worth

    @staticmethod
    def select_from_population(fitness_evaluation, population, selection_method=0, nb_parents=3):
        print(fitness_evaluation)

        if sum(fitness_evaluation) != 0:
            # -- Determine fitness ratio
            fitness_ratios = []
            for i in range(len(fitness_evaluation)):
                fitness_ratios.append(fitness_evaluation[i]/sum(fitness_evaluation)*100)

            # -- Select individuals
            parents = []

            # TODO: Implement alternative selection methods
            # -- Exit program if incorrect settings used
            if selection_method > 0:
                print("Invalid parent selection method reference")
                sys.exit()

            if selection_method == 0:
                # Elitic selection
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
            # -- Select individuals randomly
            parents = None

        return parents

    @staticmethod
    def generate_offsprings(population_size, parents, nb_random_ind, mutation_rate=0.2):
        from PhyTrade.ML_optimisation.EVOA_Optimisation.EVOA_random_gen import EVOA_random_gen
        from PhyTrade.ML_optimisation.EVOA_Optimisation.INDIVIDUAL_gen import Individual
        import random
        from copy import deepcopy

        nb_of_parameters_to_mutate = round(Individual().nb_of_parameters * mutation_rate)

        # -- Save parents to new population
        new_population = []
        for parent in parents:
            new_population.append(parent)

        # -- Generate offsprings from parents with mutations
        cycling = -1
        for _ in range(population_size - len(parents) - nb_random_ind):
            cycling += 1
            if cycling >= len(parents):
                cycling = 0

            offspring = deepcopy(parents[cycling])

            for _ in range(nb_of_parameters_to_mutate):
                parameter_type_to_modify = random.choice(list(offspring.parameter_dictionary.keys()))

                offspring = EVOA_random_gen().modify_param(offspring, parameter_type_to_modify)

            new_population.append(offspring)

        # -- Create random_ind number of random individuals and add to new population
        for _ in range(nb_random_ind):
            new_population.append(Individual())

        return new_population

    @staticmethod
    def throttle(current_generation, nb_of_generations, max_value, min_value=1, decay_function=0):
        # -- Exit program if incorrect settings used
        if decay_function > 3:
            print("Invalid throttle decay function reference")
            sys.exit()

        if decay_function == 0:       # Fixed value
            return max_value

        elif decay_function == 1:     # Linear decay
            interval = max_value - min_value
            if interval == 0:
                interval = 1

            interval_size = round(nb_of_generations/interval)
            if interval_size <= 0:
                return max_value

            throttled_value = round(-(1/interval_size)*current_generation + max_value)

            if throttled_value <= min_value:
                throttled_value = min_value

            return throttled_value

    @staticmethod
    def determine_evolving_gen_parameters(current_generation,
                                          nb_of_generations,
                                          initial_nb_parents,
                                          initial_nb_random_ind,
                                          parents_decay_function=0,
                                          random_ind_decay_function=0,
                                          print_evoa_parameters_per_gen=False):

        # ------------------ Throttle the individual count to be used by the generation
        nb_parents = EVOA_tools().throttle(current_generation,
                                           nb_of_generations,
                                           initial_nb_parents,
                                           min_value=1,
                                           decay_function=parents_decay_function)

        nb_random_ind = EVOA_tools().throttle(current_generation,
                                              nb_of_generations,
                                              initial_nb_random_ind,
                                              min_value=0,
                                              decay_function=random_ind_decay_function)

        if print_evoa_parameters_per_gen:
            print("~~~~~~~~~~~")
            print("Number of parents selected for this generation", nb_parents)
            print("Number of random individuals generated for this generation", nb_random_ind)
            print("~~~~~~~~~~~")

        return nb_parents, nb_random_ind
