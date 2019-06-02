"""
Config_1
"""
import multiprocessing
import json


class Config_0:
    def __init__(self):
        # ____________________________________________________________________________________________________
        # -- Print parameters
        self.config_name = "Test_run_2"
        self.print_evoa_parameters_per_gen = True
        self.print_evaluation_status = True

        self.plot_signal_triggers = False

        # ____________________________________________________________________________________________________
        # -- Model settings
        # self.tickers = ["AAPL", "AMZN", "INTC", "NVDA"]
        self.tickers = ["AMZN"]
        # ____________________________________________________________________________________________________
        # -- EVO_algo main parameters
        self.population_size = 20
        self.nb_of_generations = 10

        self.mutation_rate = 0.3
        self.nb_parents = 8
        self.nb_random_ind = 4

        self.exploitation_phase_len_percent = 0.15
        self.exploitation_phase_len = round(self.nb_of_generations*self.exploitation_phase_len_percent)

        self.data_slice_start_date = "2010-01-01"
        self.data_slice_size = 200
        self.data_slice_shift_per_gen = 100
        self.data_slice_cycle_count = 5

        self.data_looper = False

        # ____________________________________________________________________________________________________
        # -- Generation 0 settings
        # Set to None if random initial population wanted
        self.path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Parameter_sets\Run_2_AAPL.json"
        self.starting_parameters = json.load(open(self.path.replace('\\', '/')))
        # self.starting_parameters = None

        # -- Generations settings
        self.evaluation_methods = ["Profit", "MetaLabels"]
        self.evaluation_method = 0

        self.decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        self.parents_decay_function = 1
        self.random_ind_decay_function = 1
        self.mutation_decay_function = 1

        self.parents_selection_methods = ["Elitic"]
        self.parents_selection_method = 0

        # -- max_worker_processes
        self.max_worker_processes = multiprocessing.cpu_count() - 1

        # ____________________________________________________________________________________________________
        # -- Metalabeling settings:
        self.upper_barrier = 20
        self.lower_barrier = -20
        self.look_ahead = 10

        # ____________________________________________________________________________________________________
        # -- Benchmarking data slice settings
        self.benchmark_data_slice_start_date = "2017-01-01"
        self.benchmark_data_slice_size = 200

