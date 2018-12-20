

class GA_tools:
    @staticmethod
    def gen_initial_population(population_size=10):
        from PhyTrade.GA_optimisation.Individual_gen import Individual
        population_lst = []
        for i in range(population_size):
            population_lst.append(Individual())

        return population_lst

    @staticmethod
    def evaluate_population(population_lst, data_slice_info, max_worker_threads=8,
                            print_evaluation_status=False, plot_3=False):
        from PhyTrade.Trading_bots.Tradebot_v3 import Tradebot_v3
        from PhyTrade.Tools.MULTI_THREADING_tools import multi_thread_loops

        performance_lst = []

        # -- List based evaluation
        for i in range(len(population_lst)):
            population_lst[i].perform_trade_run(data_slice_info, plot_3=plot_3)
            performance_lst.append(population_lst[i].account.net_worth_history[-1])

            if print_evaluation_status:
                print("Parameter set", i + 1, "evaluation completed")

        # -- Multi-thread evaluation
        # def evaluation_func(item):
        #     performance_lst.append(Tradebot_v3(item.parameter_dictionary, data_slice_info).account.net_worth_history[-1])

        # multi_thread_loops(population_lst, evaluation_func, max_worker_threads=max_worker_threads)

        # performance_lst = MATH().normalise_zero_one(performance_lst)
        return performance_lst

    @staticmethod
    def select_from_population(fitness_evaluation, population, selection_method=0, nb_parents=3):

        # -- Determine fitness ratio
        fitness_ratios = []

        for i in range(len(fitness_evaluation)):
            fitness_ratios.append(fitness_evaluation[i]/sum(fitness_evaluation)*100)

        # -- Select individuals
        parents = []

        if selection_method == 0:
            scanned_fitness_ratios = fitness_ratios

            for i in range(nb_parents):
                individual = scanned_fitness_ratios.index(max(scanned_fitness_ratios))
                parents.append(population[individual])

                population.pop(individual)
                scanned_fitness_ratios.pop(individual)

        return parents

    @staticmethod
    def generate_offsprings(population_size, nb_parents, parents, random_ind, mutation_rate=0.2):
        from PhyTrade.GA_optimisation.GA_random_gen import GA_random_gen
        from PhyTrade.GA_optimisation.Individual_gen import Individual
        import random
        from copy import deepcopy

        ga_random_gen = GA_random_gen

        nb_of_parameters_to_mutate = round(Individual().nb_of_parameters * mutation_rate)

        # -- Save parents to new population
        new_population = []
        for parent in parents:
            new_population.append(parent)

        # -- Generate offsprings from parents with mutations
        cycling = -1
        for i in range(population_size-nb_parents-random_ind):

            cycling += 1
            if cycling >= nb_parents:
                cycling = 0

            offspring = deepcopy(parents[cycling])

            for j in range(nb_of_parameters_to_mutate):
                parameter_type_to_modify = random.choice(list(offspring.parameter_dictionary.keys()))

                if parameter_type_to_modify == "timeframe":
                    parameter = random.choice(list(offspring.parameter_dictionary["timeframe"]))

                    offspring.parameter_dictionary["timeframe"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["timeframe"][parameter])

                elif parameter_type_to_modify == "rsi_standard_upper_thresholds":
                    parameter = random.choice(list(offspring.parameter_dictionary["rsi_standard_upper_thresholds"]))

                    offspring.parameter_dictionary["rsi_standard_upper_thresholds"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["rsi_standard_upper_thresholds"][parameter])

                elif parameter_type_to_modify == "rsi_standard_lower_thresholds":
                    parameter = random.choice(list(offspring.parameter_dictionary["rsi_standard_lower_thresholds"]))

                    offspring.parameter_dictionary["rsi_standard_lower_thresholds"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["rsi_standard_lower_thresholds"][parameter])

                elif parameter_type_to_modify == "smoothing_factors":
                    parameter = random.choice(list(offspring.parameter_dictionary["smoothing_factors"]))

                    offspring.parameter_dictionary["smoothing_factors"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["smoothing_factors"][parameter])

                elif parameter_type_to_modify == "amplification_factor":
                    parameter = random.choice(list(offspring.parameter_dictionary["amplification_factor"]))

                    offspring.parameter_dictionary["amplification_factor"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["amplification_factor"][parameter])

                elif parameter_type_to_modify == "weights":
                    parameter = random.choice(list(offspring.parameter_dictionary["weights"]))

                    offspring.parameter_dictionary["weights"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["weights"][parameter])
            new_population.append(offspring)

        # -- Create random_ind number of random individuals and add to new population
        for i in range(random_ind):
            new_population.append(Individual())

        return new_population

    @staticmethod
    def throttle(current_generation, nb_of_generations, max_value, min_value=1, decay_function=0):

        if decay_function == 0:
            return max_value

        elif decay_function == 1:     # Linear decrease
            interval = max_value - min_value

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
                                          print_ga_parameters_per_gen=False):

        # ------------------ Define the data slice to be used by the generation
        # data_slice_info.get_next_data_slice()
        data_slice_info.get_shifted_data_slice()

        # ------------------ Throttle the individual count to be used by the generation
        nb_parents = GA_tools().throttle(current_generation,
                                         nb_of_generations,
                                         initial_nb_parents,
                                         min_value=1,
                                         decay_function=parents_decay_function)

        nb_random_ind = GA_tools().throttle(current_generation,
                                            nb_of_generations,
                                            initial_nb_random_ind,
                                            min_value=0,
                                            decay_function=random_ind_decay_function)

        if print_ga_parameters_per_gen:
            print("~~~~~~~~~~~")
            print("Data slice analysed:", data_slice_info.start_index, "-->", data_slice_info.stop_index, "\n")
            print("Number of parents selected for this generation", nb_parents)
            print("Number of random individuals generated for this generation", nb_random_ind)
            print("~~~~~~~~~~~")

        return data_slice_info, nb_parents, nb_random_ind































