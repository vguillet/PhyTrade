"""
Config_1
"""
import multiprocessing


class Config_0:
    def __init__(self):
        # ____________________________________________________________________________________________________
        # -- Print parameters
        self.config_name = "Test configuration"
        self.print_evoa_parameters_per_gen = True
        self.print_evaluation_status = True

        self.plot_signal_triggers = False

        # ____________________________________________________________________________________________________
        # EVO_algo main parameters
        self.population_size = 5
        self.nb_of_generations = 10

        self.mutation_rate = 0.5
        self.nb_parents = 2
        self.nb_random_ind = 1

        self.exploitation_phase_len = 1

        self.data_slice_start_index = -7000
        self.data_slice_size = 200
        self.data_slice_shift_per_gen = 100

        # ____________________________________________________________________________________________________
        # -- Generations settings
        self.decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]

        self.parents_decay_function = 1
        self.random_ind_decay_function = 1

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
        self.benchmark_data_slice_start = -453
        self.benchmark_data_slice_stop = 252

