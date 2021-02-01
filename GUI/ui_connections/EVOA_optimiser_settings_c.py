
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import datetime

# Libs

# Own modules
from GUI.Tools.Settings_to_json import record_settings

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

##################################################################################################################


def save_EVOA_optimiser_settings(ui, location="Current_settings", name=""):
    EVOA_optimiser_settings = {}

    # ___________________________ Optimisation parameters ____________________
    EVOA_optimiser_settings["config_name"] = ui.EVOA_optimisation_config_name.text()

    # ---- Multiprocessing settings
    EVOA_optimiser_settings["multiprocessing"] = str(ui.EVOA_optimisation_multiprocessing.currentText())

    # ___________________________ Print/plot parameters ______________________
    EVOA_optimiser_settings["print_evoa_parameters_per_gen"] = ui.EVOA_optimisation_print_evoa_parameters_per_gen.isChecked()
    EVOA_optimiser_settings["print_evaluation_status"] = ui.EVOA_optimisation_print_evaluation_status.isChecked()
    EVOA_optimiser_settings["print_generation_info"] = ui.EVOA_optimisation_print_generation_info.isChecked()
    EVOA_optimiser_settings["print_trade_process"] = ui.EVOA_optimisation_print_trade_process.isChecked()

    EVOA_optimiser_settings["plot_best_individual_eco_model_results"] = ui.EVOA_optimisation_plot_best_individual_eco_model_results.isChecked()
    EVOA_optimiser_settings["plot_eco_model_results"] = ui.EVOA_optimisation_plot_eco_model_results.isChecked()

    # ___________________________ EVO_algo main parameters ___________________
    # ---- Data slice parameters
    # TODO: Connect parameter black list ticker boxes
    #EVOA_optimiser_settings["parameter_blacklist"] = ui.

    # ---- Population parameters
    EVOA_optimiser_settings["nb_of_generations"] = ui.EVOA_optimisation_nb_of_generations.value()
    EVOA_optimiser_settings["population_size"] = ui.EVOA_optimisation_population_size.value()

    EVOA_optimiser_settings["nb_parents"] = ui.EVOA_optimisation_nb_parents.value()
    EVOA_optimiser_settings["nb_random_ind"] = ui.EVOA_optimisation_nb_random_ind.value()

    EVOA_optimiser_settings["mutation_rate"] = ui.EVOA_optimisation_mutation_rate.value()
    EVOA_optimiser_settings["nb_parents_in_next_gen"] = ui.EVOA_optimisation_nb_parents_in_next_gen.value()

    EVOA_optimiser_settings["data_slice_cycle_count"] = ui.EVOA_optimisation_data_slice_cycle_count.value()
    EVOA_optimiser_settings["data_slice_shift_per_gen"] = ui.EVOA_optimisation_data_slice_shift_per_gen.value()
    EVOA_optimiser_settings["data_looper"] = str(ui.EVOA_optimisation_data_looper.isChecked())

    # -- Generations settings
    EVOA_optimiser_settings["exploitation_phase_len_percent"] = ui.EVOA_optimisation_exploitation_phase_len_percent.value()

    EVOA_optimiser_settings["evaluation_method"] = str(ui.EVOA_optimisation_evaluation_method.currentText())

    EVOA_optimiser_settings["parents_decay_function"] = str(ui.EVOA_optimisation_parents_decay_function.currentText())
    EVOA_optimiser_settings["random_ind_decay_function"] = str(ui.EVOA_optimisation_random_ind_decay_function.currentText())
    EVOA_optimiser_settings["mutation_decay_function"] = str(ui.EVOA_optimisation_mutation_decay_function.currentText())

    EVOA_optimiser_settings["parents_selection_method"] = str(ui.EVOA_optimisation_parents_selection_method.currentText())

    # ___________________________ Generation 0 parameters ____________________
    # -- Starting parameters
    EVOA_optimiser_settings["starting_parameters"] = ui.EVOA_optimisation_starting_parameters.text()

    record_settings(EVOA_optimiser_settings, location, name="EVOA_optimiser_settings"+"_"+name)
