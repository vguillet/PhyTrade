

class Metalabeling_settings:
    # =============================== METALABELS SETTINGS =========================
    def gen_metalabels_settings(self):
        # -- Metalabeling settings:
        self.metalabeling_settings = ["Peak", "Simple", "Hybrid"]
        self.metalabeling_setting = 0

        self.upper_barrier = 20
        self.lower_barrier = -20
        self.look_ahead = 20

    # =============================== EVOA METALABELS SETTINGS ====================
    def gen_evoa_metalabels_settings(self):
        import multiprocessing
        # ___________________________ Optimisation parameters ____________________
        # ---- Multiprocessing settings
        self.multiprocessing = False
        self.max_process_count = multiprocessing.cpu_count() - 1

        # ___________________________ Print/plot parameters ______________________
        self.print_evoa_parameters_per_gen = True
        self.print_evaluation_status = False

        self.plot_best_individual_eco_model_results = True
        self.plot_eco_model_results = False

        # ___________________________ EVO_algo main parameters ___________________
        self.population_size = 30
        self.nb_of_generations = 20

        self.mutation_rate = 0.5
        self.nb_parents = 10
        self.nb_random_ind = 3

        # -- Generations settings
        self.evaluation_methods = ["Profit", "MetaLabels", "MetaLabels bs", "MetaLabels avg", "Buy count", "Sell count",
                                   "Transaction count"]
        self.evaluation_method = 0

        self.decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        self.parents_decay_function = 1
        self.random_ind_decay_function = 1
        self.mutation_decay_function = 1

        self.parents_selection_methods = ["Elitic"]
        self.parents_selection_method = 0
