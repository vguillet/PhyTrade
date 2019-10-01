
##################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from GUI_1_1.Tools.Settings_to_json import record_settings

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

##################################################################################################################

def get_EVOA_metalabels_settings(ui):
    EVOA_metalabeling_settings = {}

    # ___________________________ Optimisation parameters ____________________
    EVOA_metalabeling_settings["config_name"] = ui.config_name_2.text()

    # ---- Multiprocessing settings
    EVOA_metalabeling_settings["multiprocessing"] = str(ui.multiprocessing_2.currentText())

    # ___________________________ Print/plot parameters ______________________
    EVOA_metalabeling_settings["print_evoa_parameters_per_gen"] = ui.print_evoa_parameters_per_gen_2.isChecked()
    EVOA_metalabeling_settings["print_evaluation_status"] = ui.print_evaluation_status_2.isChecked()
    EVOA_metalabeling_settings["print_generation_info"] = ui.print_generation_info_2.isChecked()
    EVOA_metalabeling_settings["print_trade_process"] = ui.print_trade_process_2.isChecked()

    EVOA_metalabeling_settings["plot_best_individual_eco_model_results"] = ui.plot_best_individual_eco_model_results_2.isChecked()
    EVOA_metalabeling_settings["plot_eco_model_results"] = ui.plot_eco_model_results_2.isChecked()

    # ___________________________ EVO_algo main parameters ___________________
    # ---- Data slice parameters
    # TODO: Connect parameter black list ticker boxes
    # EVOA_metalabeling_settings["parameter_blacklist"] = ui.

    # ---- Population parameters
    EVOA_metalabeling_settings["nb_of_generations"] = ui.nb_of_generations_2.value()
    EVOA_metalabeling_settings["population_size"] = ui.population_size_2.value()

    EVOA_metalabeling_settings["nb_parents"] = ui.nb_parents_2.value()
    EVOA_metalabeling_settings["nb_random_ind"] = ui.nb_random_ind_2.value()

    EVOA_metalabeling_settings["mutation_rate"] = ui.mutation_rate_2.value()
    EVOA_metalabeling_settings["nb_parents_in_next_gen"] = ui.nb_parents_in_next_gen_2.value()

    # -- Generations settings
    EVOA_metalabeling_settings["exploitation_phase_len_percent"] = ui.exploitation_phase_len_percent_2.value()

    EVOA_metalabeling_settings["evaluation_method"] = str(ui.evaluation_method_2.currentText())

    EVOA_metalabeling_settings["parents_decay_function"] = str(ui.parents_decay_function_2.currentText())
    EVOA_metalabeling_settings["random_ind_decay_function"] = str(ui.random_ind_decay_function_2.currentText())
    EVOA_metalabeling_settings["mutation_decay_function"] = str(ui.mutation_decay_function_2.currentText())

    EVOA_metalabeling_settings["parents_selection_method"] = str(ui.parents_selection_method_2.currentText())

    # ___________________________ Generation 0 parameters ____________________
    # -- Starting parameters
    EVOA_metalabeling_settings["starting_parameters"] = ui.starting_parameters_2.text()

    record_settings(EVOA_metalabeling_settings, "Current_settings", name="EVOA_metalabeling_settings")
