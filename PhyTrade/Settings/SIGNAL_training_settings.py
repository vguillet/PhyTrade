from PhyTrade.Data_Collection_preparation.Fetch_parameter_set import fetch_parameter_set
import multiprocessing


class Signal_training_settings:
    # =============================== EVOA SETTINGS ===============================
    def gen_evoa_settings(self):
        # ___________________________ Optimisation parameters ____________________
        self.config_name = "Run_6"

        # ---- Multiprocessing settings
        self.multiprocessing = False
        self.max_process_count = multiprocessing.cpu_count() - 1

        # ___________________________ Print/plot parameters ______________________
        self.print_evoa_parameters_per_gen = True
        self.print_evaluation_status = False

        self.plot_best_individual_eco_model_results = True
        self.plot_eco_model_results = False

        # ___________________________ EVO_algo main parameters ___________________
        # ---- Data slice parameters
        self.data_slice_shift_per_gen = 12
        self.data_slice_cycle_count = 10

        self.data_looper = False

        # ---- Population parameters
        self.population_size = 30
        self.nb_of_generations = 40

        self.mutation_rate = 0.5
        self.nb_parents = 10
        self.nb_random_ind = 3
        
        self.nb_parents_in_next_gen = 5

        # -- Generations settings
        self.exploitation_phase_len_percent = 0.15
        self.exploitation_phase_len = round(self.nb_of_generations*self.exploitation_phase_len_percent)

        self.evaluation_methods = ["Net Worth", "MetaLabels", "MetaLabels bs", "MetaLabels avg", "Buy count", "Sell count", "Transaction count"]
        self.evaluation_method = 0

        self.decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        self.parents_decay_function = 1
        self.random_ind_decay_function = 1
        self.mutation_decay_function = 1

        self.parents_selection_methods = ["Elitic"]
        self.parents_selection_method = 0

        # ___________________________ Generation 0 parameters ____________________
        # -- Starting parameters
        # --> Set to None if random initial population wanted
        self.starting_parameters = None
