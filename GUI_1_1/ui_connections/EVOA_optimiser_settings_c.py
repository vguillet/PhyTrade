
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import datetime

# Libs

# Own modules
from GUI_1_1.Tools.Settings_to_json import record_settings

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

##################################################################################################################


def save_EVOA_optimiser_settings(ui, location="Current_settings", name=""):
    EVOA_optimiser_settings = {}

    # ___________________________ Optimisation parameters ____________________
    EVOA_optimiser_settings["config_name"] = ui.config_name_1.text()

    # ---- Multiprocessing settings
    EVOA_optimiser_settings["multiprocessing"] = str(ui.multiprocessing_1.currentText())

    # ___________________________ Print/plot parameters ______________________
    EVOA_optimiser_settings["print_evoa_parameters_per_gen"] = ui.print_evoa_parameters_per_gen_1.isChecked()
    EVOA_optimiser_settings["print_evaluation_status"] = ui.print_evaluation_status_1.isChecked()
    EVOA_optimiser_settings["print_generation_info"] = ui.print_generation_info_1.isChecked()
    EVOA_optimiser_settings["print_trade_process"] = ui.print_trade_process_1.isChecked()

    EVOA_optimiser_settings["plot_best_individual_eco_model_results"] = ui.plot_best_individual_eco_model_results_1.isChecked()
    EVOA_optimiser_settings["plot_eco_model_results"] = ui.plot_eco_model_results_1.isChecked()

    # ___________________________ EVO_algo main parameters ___________________
    # ---- Data slice parameters
    # TODO: Connect parameter black list ticker boxes
    #EVOA_optimiser_settings["parameter_blacklist"] = ui.

    # ---- Population parameters
    EVOA_optimiser_settings["nb_of_generations"] = ui.nb_of_generations_1.value()
    EVOA_optimiser_settings["population_size"] = ui.population_size_1.value()

    EVOA_optimiser_settings["nb_parents"] = ui.nb_parents_1.value()
    EVOA_optimiser_settings["nb_random_ind"] = ui.nb_random_ind_1.value()

    EVOA_optimiser_settings["mutation_rate"] = ui.mutation_rate_1.value()
    EVOA_optimiser_settings["nb_parents_in_next_gen"] = ui.nb_parents_in_next_gen_1.value()

    EVOA_optimiser_settings["data_slice_cycle_count"] = ui.data_slice_cycle_count_1.value()
    EVOA_optimiser_settings["data_slice_shift_per_gen"] = ui.data_slice_shift_per_gen_1.value()
    EVOA_optimiser_settings["data_looper"] = str(ui.data_looper_1.currentText())

    # -- Generations settings
    EVOA_optimiser_settings["exploitation_phase_len_percent"] = ui.exploitation_phase_len_percent_1.value()

    EVOA_optimiser_settings["evaluation_method"] = str(ui.evaluation_method_1.currentText())

    EVOA_optimiser_settings["parents_decay_function"] = str(ui.parents_decay_function_1.currentText())
    EVOA_optimiser_settings["random_ind_decay_function"] = str(ui.random_ind_decay_function_1.currentText())
    EVOA_optimiser_settings["mutation_decay_function"] = str(ui.mutation_decay_function_1.currentText())

    EVOA_optimiser_settings["parents_selection_method"] = str(ui.parents_selection_method_1.currentText())

    # ___________________________ Generation 0 parameters ____________________
    # -- Starting parameters
    EVOA_optimiser_settings["starting_parameters"] = ui.starting_parameters_1.text()

    record_settings(EVOA_optimiser_settings, location, name="EVOA_optimiser_settings"+"_"+name)

