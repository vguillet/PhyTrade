import multiprocessing


class EVOA_settings:
    # =============================== EVOA SETTINGS ===============================
    def gen_evoa_settings(self):
        # ___________________________ Optimisation parameters ____________________
        self.config_name = "Run_6"
        self.multiprocessing = False

        self.tickers = ["AAPL", "INTC", "NVDA", "AMZN"]
        # self.tickers = ["AAPL"]

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

        self.exploitation_phase_len_percent = 0.15
        self.exploitation_phase_len = round(self.nb_of_generations*self.exploitation_phase_len_percent)

        self.data_slice_start_date = "2017-01-03"
        self.data_slice_size = 24
        self.data_slice_shift_per_gen = 12
        self.data_slice_cycle_count = 5

        self.data_looper = False

        # TODO: Add slize size auto scaling according to generation count/cycle count and start/end date
        self.end_date = "2019-01-02"
        # self.end_date = None

        # ___________________________ Generation 0 parameters ____________________
        # -- Starting parameters
        # --> Set to None if random initial population wanted
        # self.starting_parameters = json.load(open(r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Parameter_sets\Run_4_AAPL.json".replace('\\', '/')))
        self.starting_parameters = None

        # -- Generations settings
        self.evaluation_methods = ["Profit", "MetaLabels", "MetaLabels bs", "MetaLabels avg", "Buy count", "Sell count", "Transaction count"]
        self.evaluation_method = 0

        self.decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        self.parents_decay_function = 1
        self.random_ind_decay_function = 1
        self.mutation_decay_function = 1

        self.parents_selection_methods = ["Elitic"]
        self.parents_selection_method = 0

        # -- max_worker_processes
        self.max_worker_processes = multiprocessing.cpu_count() - 1

        # ___________________________ Benchmark parameters _______________________
        # -- Benchmarking data slice settings
        self.benchmark_data_slice_start_date = "2019-01-02"
        self.benchmark_data_slice_size = 200
