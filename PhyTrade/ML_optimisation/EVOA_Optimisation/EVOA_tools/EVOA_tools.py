

class EVOA_tools:
    @staticmethod
    def gen_initial_population(population_size=10):
        from PhyTrade.ML_optimisation.EVOA_Optimisation.Individual_gen import Individual

        population_lst = []
        for i in range(population_size):
            population_lst.append(Individual())

        return population_lst

    @staticmethod
    def evaluate_population(population_lst, data_slice_info, max_worker_processes=1,
                            print_evaluation_status=False, plot_3=False):

        from PhyTrade.ML_optimisation.EVOA_Optimisation.EVOA_tools.EVOA_benchmark_tool import Confusion_matrix_analysis
        accuracies_achieved = []
        confusion_matrix_analysis = []

        # -- List based evaluation
        for i in range(len(population_lst)):

            if print_evaluation_status:
                print("\n ----------------------------------------------")
                print("Parameter set", i + 1, "evaluation completed:\n")

            population_lst[i].gen_economic_model(data_slice_info, plot_3=plot_3)
            # population_lst[i].perform_trade_run()

            individual_confusion_matrix_analysis = Confusion_matrix_analysis(population_lst[i].analysis.big_data.Major_spline.trade_signal,
                                                                             data_slice_info.metalabels.close_values_metalabels,
                                                                             print_benchmark_results=print_evaluation_status)

            confusion_matrix_analysis.append(individual_confusion_matrix_analysis)
            accuracies_achieved.append(individual_confusion_matrix_analysis.overall_accuracy_bs)

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

        return accuracies_achieved, confusion_matrix_analysis

    @staticmethod
    def select_from_population(fitness_evaluation, population, selection_method=0, nb_parents=3):

        # -- Determine fitness ratio
        fitness_ratios = []

        for i in range(len(fitness_evaluation)):
            fitness_ratios.append(fitness_evaluation[i]/sum(fitness_evaluation)*100)

        # -- Select individuals
        parents = []

        if selection_method == 0:
            # Elitic selection
            scanned_fitness_ratios = fitness_ratios

            best_individual_printed = False

            for _ in range(nb_parents):
                individual = scanned_fitness_ratios.index(max(scanned_fitness_ratios))
                parents.append(population[individual])
                if best_individual_printed is False:
                    print("Best Individual number from previous generation:", individual)
                    best_individual_printed = True

                population.pop(individual)
                scanned_fitness_ratios.pop(individual)

        return parents

    @staticmethod
    def generate_offsprings(population_size, nb_parents, parents, nb_random_ind, mutation_rate=0.2):
        from PhyTrade.ML_optimisation.EVOA_Optimisation.EVOA_random_gen import EVOA_random_gen
        from PhyTrade.ML_optimisation.EVOA_Optimisation.Individual_gen import Individual
        import random
        from copy import deepcopy

        nb_of_parameters_to_mutate = round(Individual().nb_of_parameters * mutation_rate)

        # -- Save parents to new population
        new_population = []
        for parent in parents:
            new_population.append(parent)

        # -- Generate offsprings from parents with mutations
        cycling = -1
        for i in range(population_size - nb_parents - nb_random_ind):

            cycling += 1
            if cycling >= nb_parents:
                cycling = 0

            offspring = deepcopy(parents[cycling])

            for j in range(nb_of_parameters_to_mutate):
                parameter_type_to_modify = random.choice(list(offspring.parameter_dictionary.keys()))

                offspring = EVOA_random_gen().modify_param(offspring, parameter_type_to_modify)

            new_population.append(offspring)

        # -- Create random_ind number of random individuals and add to new population
        for i in range(nb_random_ind):
            new_population.append(Individual())

        return new_population

    @staticmethod
    def throttle(current_generation, nb_of_generations, max_value, min_value=1, decay_function=0):

        if decay_function == 0:
            return max_value

        elif decay_function == 1:     # Linear decrease
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
    def determine_evolving_gen_parameters(data_slice_info,
                                          current_generation,
                                          nb_of_generations,
                                          initial_nb_parents,
                                          initial_nb_random_ind,
                                          parents_decay_function=0,
                                          random_ind_decay_function=0,
                                          print_evoa_parameters_per_gen=False):

        # ------------------ Define the data slice to be used by the generation
        # data_slice_info.get_next_data_slice()
        data_slice_info.get_shifted_data_slice()

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
            print("Data slice analysed:", data_slice_info.start_index, "-->", data_slice_info.stop_index, "\n")
            print("Number of parents selected for this generation", nb_parents)
            print("Number of random individuals generated for this generation", nb_random_ind)
            print("~~~~~~~~~~~")

        return data_slice_info, nb_parents, nb_random_ind
