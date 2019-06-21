

class Metalabeling_settings:
    # =============================== METALABELING SETTINGS =======================
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

        # TODO: Add slize size auto scaling according to generation count/cycle count and start/end date
        self.start_date = "2017-01-03"
        self.end_date = None

        self.data_slice_size = 24
        self.data_slice_cycle_count = 5

        self.data_looper = False

        # ___________________________ Generation 0 parameters ____________________
        # -- Starting parameters
        # --> Set to None if random initial population wanted
        # self.starting_parameters = json.load(open(r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Parameter_sets\Run_4_AAPL.json".replace('\\', '/')))
        self.starting_parameters = None

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
