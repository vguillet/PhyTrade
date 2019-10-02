
##################################################################################################################
"""
Contains settings for running the optimiser
"""

# Built-in/Generic Imports
import json
import multiprocessing

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class Optimiser_settings:
    # =============================== EVOA SETTINGS ===============================
    def gen_evoa_settings(self):
        EVOA_optimiser_settings = json.load(open(r"C:\Users\Victor Guillet\Google Drive\Computer science\2-Programing\Repos\Python\Steffegium\Data\Settings\Current_settings\EVOA_optimiser_settings_.json"))

        # ___________________________ Optimisation parameters ____________________
        self.config_name = EVOA_optimiser_settings["config_name"]
        self.optimiser_setting = 1  # Optimiser run mode

        # ---- Multiprocessing settings
        self.multiprocessing = EVOA_optimiser_settings["multiprocessing"]
        self.max_process_count = multiprocessing.cpu_count() - 1

        # ___________________________ Print/plot parameters ______________________
        self.print_evoa_parameters_per_gen = EVOA_optimiser_settings["print_evoa_parameters_per_gen"]
        self.print_evaluation_status = EVOA_optimiser_settings["print_evaluation_status"]
        self.print_generation_info = EVOA_optimiser_settings["print_generation_info"]
        self.print_trade_process = EVOA_optimiser_settings["print_trade_process"]

        self.plot_best_individual_eco_model_results = EVOA_optimiser_settings["plot_best_individual_eco_model_results"]
        self.plot_eco_model_results = EVOA_optimiser_settings["plot_eco_model_results"]

        # ___________________________ EVO_algo main parameters ___________________
        # ---- Data slice parameters
        # TODO: Connect blacklist setting to GUI
        self.parameter_blacklist = ["general_settings"]

        # ---- Population parameters
        self.nb_of_generations = EVOA_optimiser_settings["nb_of_generations"]
        self.population_size = EVOA_optimiser_settings["population_size"]

        self.nb_parents = EVOA_optimiser_settings["nb_parents"]
        self.nb_random_ind = EVOA_optimiser_settings["nb_random_ind"]

        self.mutation_rate = EVOA_optimiser_settings["mutation_rate"]
        self.nb_parents_in_next_gen = EVOA_optimiser_settings["nb_parents_in_next_gen"]
        self.data_slice_cycle_count = EVOA_optimiser_settings["data_slice_cycle_count"]
        self.data_slice_shift_per_gen = EVOA_optimiser_settings["data_slice_shift_per_gen"]
        self.data_looper = EVOA_optimiser_settings["data_looper"]

        # -- Generations settings
        self.exploitation_phase_len_percent = EVOA_optimiser_settings["exploitation_phase_len_percent"]
        self.exploitation_phase_len = round(self.nb_of_generations*self.exploitation_phase_len_percent)

        self.evaluation_methods = ["Net Worth", "MetaLabels", "MetaLabels bs", "MetaLabels avg", "Buy count", "Sell count", "Transaction count"]
        self.evaluation_method = self.evaluation_methods.index(EVOA_optimiser_settings["evaluation_method"])

        self.decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        self.parents_decay_function = self.decay_functions.index(EVOA_optimiser_settings["parents_decay_function"])
        self.random_ind_decay_function = self.decay_functions.index(EVOA_optimiser_settings["random_ind_decay_function"])
        self.mutation_decay_function = self.decay_functions.index(EVOA_optimiser_settings["mutation_decay_function"])

        self.parents_selection_methods = ["Elitic"]
        self.parents_selection_method = self.parents_selection_methods.index(EVOA_optimiser_settings["parents_selection_method"])

        # ___________________________ Generation 0 parameters ____________________
        # -- Starting parameters
        # --> Set to None if random initial population wanted
        if len(EVOA_optimiser_settings["starting_parameters"]) == 0:
            self.starting_parameters = EVOA_optimiser_settings["starting_parameters"]
        else:
            self.starting_parameters = None

    # =============================== EVOA METALABELS SETTINGS ====================
    def gen_evoa_metalabels_settings(self):
        EVOA_metalabels_settings = json.load(open(r"C:\Users\Victor Guillet\Google Drive\Computer science\2-Programing\Repos\Python\Steffegium\Data\Settings\Current_settings\EVOA_metalabels_settings_.json"))

        # ___________________________ Optimisation parameters ____________________
        self.config_name = EVOA_metalabels_settings["config_name"]
        self.optimiser_setting = 2

        # ---- Multiprocessing settings
        self.multiprocessing = EVOA_metalabels_settings["multiprocessing"]
        self.max_process_count = multiprocessing.cpu_count() - 1

        # ___________________________ Print/plot parameters ______________________
        self.print_evoa_parameters_per_gen = EVOA_metalabels_settings["print_evoa_parameters_per_gen"]
        self.print_evaluation_status = EVOA_metalabels_settings["print_evaluation_status"]
        self.print_generation_info = EVOA_metalabels_settings["print_generation_info"]
        self.print_trade_process = EVOA_metalabels_settings["print_trade_process"]

        self.plot_best_individual_eco_model_results = EVOA_metalabels_settings["plot_best_individual_eco_model_results"]
        self.plot_eco_model_results = EVOA_metalabels_settings["plot_eco_model_results"]

        # ___________________________ EVO_algo main parameters ___________________
        # ---- Data slice parameters
        # TODO: Connect blacklist setting to GUI
        self.parameter_blacklist = ["general_settings"]

        # ---- Population parameters
        self.nb_of_generations = EVOA_metalabels_settings["nb_of_generations"]
        self.population_size = EVOA_metalabels_settings["population_size"]

        self.nb_parents = EVOA_metalabels_settings["nb_parents"]
        self.nb_random_ind = EVOA_metalabels_settings["nb_random_ind"]

        self.mutation_rate = EVOA_metalabels_settings["mutation_rate"]
        self.nb_parents_in_next_gen = EVOA_metalabels_settings["nb_parents_in_next_gen"]

        # -- Generations settings
        self.exploitation_phase_len_percent = EVOA_metalabels_settings["exploitation_phase_len_percent"]
        self.exploitation_phase_len = round(self.nb_of_generations*self.exploitation_phase_len_percent)

        self.evaluation_methods = ["Profit", "MetaLabels", "MetaLabels bs", "MetaLabels avg", "Buy count", "Sell count",
                                   "Transaction count"]
        self.evaluation_method = EVOA_metalabels_settings["evaluation_method"]

        self.decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        self.parents_decay_function = EVOA_metalabels_settings["parents_decay_function"]
        self.random_ind_decay_function = EVOA_metalabels_settings["random_ind_decay_function"]
        self.mutation_decay_function = EVOA_metalabels_settings["mutation_decay_function"]

        self.parents_selection_methods = ["Elitic"]
        self.parents_selection_method = EVOA_metalabels_settings["parents_selection_method"]

        # ___________________________ Generation 0 parameters ____________________
        # -- Starting parameters
        # --> Set to None if random initial population wanted
        if len(EVOA_metalabels_settings["starting_parameters"]) == 0:
            self.starting_parameters = EVOA_metalabels_settings["starting_parameters"]
        else:
            self.starting_parameters = None
