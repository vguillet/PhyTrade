
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


def save_EVOA_metalabels_settings(ui, location="Current_settings", name=""):
    EVOA_metalabels_settings = {}

    # ___________________________ Optimisation parameters ____________________
    EVOA_metalabels_settings["config_name"] = ui.EVOA_metalabeling_config_name.text()

    # ---- Multiprocessing settings
    EVOA_metalabels_settings["multiprocessing"] = str(ui.EVOA_metalabeling_multiprocessing.currentText())

    # ___________________________ Print/plot parameters ______________________
    EVOA_metalabels_settings["print_evoa_parameters_per_gen"] = ui.EVOA_metalabeling_print_evoa_parameters_per_gen.isChecked()
    EVOA_metalabels_settings["print_evaluation_status"] = ui.EVOA_metalabeling_print_evaluation_status.isChecked()
    EVOA_metalabels_settings["print_generation_info"] = ui.EVOA_metalabeling_print_generation_info.isChecked()
    EVOA_metalabels_settings["print_trade_process"] = ui.EVOA_metalabeling_print_trade_process.isChecked()

    EVOA_metalabels_settings["plot_best_individual_eco_model_results"] = ui.EVOA_metalabeling_plot_best_individual_eco_model_results.isChecked()
    EVOA_metalabels_settings["plot_eco_model_results"] = ui.EVOA_metalabeling_plot_eco_model_results.isChecked()

    # ___________________________ EVO_algo main parameters ___________________
    # ---- Data slice parameters
    # TODO: Connect parameter black list ticker boxes
    # EVOA_metalabels_settings["parameter_blacklist"] = ui.

    # ---- Population parameters
    EVOA_metalabels_settings["nb_of_generations"] = ui.EVOA_metalabeling_nb_of_generations.value()
    EVOA_metalabels_settings["population_size"] = ui.population_size.value()

    EVOA_metalabels_settings["nb_parents"] = ui.EVOA_metalabeling_nb_parents.value()
    EVOA_metalabels_settings["nb_random_ind"] = ui.EVOA_metalabeling_nb_random_ind.value()

    EVOA_metalabels_settings["mutation_rate"] = ui.EVOA_metalabeling_mutation_rate.value()
    EVOA_metalabels_settings["nb_parents_in_next_gen"] = ui.EVOA_metalabeling_nb_parents_in_next_gen.value()

    # -- Generations settings
    EVOA_metalabels_settings["exploitation_phase_len_percent"] = ui.EVOA_metalabeling_exploitation_phase_len_percent.value()

    EVOA_metalabels_settings["evaluation_method"] = str(ui.EVOA_metalabeling_evaluation_method.currentText())

    EVOA_metalabels_settings["parents_decay_function"] = str(ui.EVOA_metalabeling_parents_decay_function.currentText())
    EVOA_metalabels_settings["random_ind_decay_function"] = str(ui.EVOA_metalabeling_random_ind_decay_function.currentText())
    EVOA_metalabels_settings["mutation_decay_function"] = str(ui.EVOA_metalabeling_mutation_decay_function.currentText())

    EVOA_metalabels_settings["parents_selection_method"] = str(ui.EVOA_metalabeling_parents_selection_method.currentText())

    # ___________________________ Generation 0 parameters ____________________
    # -- Starting parameters
    EVOA_metalabels_settings["starting_parameters"] = ui.EVOA_metalabeling_starting_parameters.text()

    record_settings(EVOA_metalabels_settings, location, name="EVOA_metalabels_settings"+"_"+name)
