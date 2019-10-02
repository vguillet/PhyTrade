
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


def get_general_trade_sim_settings(ui, location="Current_settings", name=""):
    trade_sim_general_settings = {}

    # ___________________________ Simulation parameters ______________________
    trade_sim_general_settings["simulation_name"] = ui.simulation_name.text()
    trade_sim_general_settings["nb_data_slices"] = ui.nb_data_slices.value()

    # ___________________________ Print/plot parameters ______________________
    trade_sim_general_settings["print_trade_process"] = ui.print_trade_process.isChecked()
    trade_sim_general_settings["plot_eco_model_results_sim"] = ui.plot_eco_model_results_sim.isChecked()

    # ___________________________ Investment settings ________________________
    trade_sim_general_settings["investment_settings"] = str(ui.investment_settings.currentText())
    trade_sim_general_settings["cash_in_settings"] = str(ui.cash_in_settings.currentText())

    # Max --> Min
    trade_sim_general_settings["max_investment_per_trade_percent"] = ui.max_investment_per_trade_percent.value()
    trade_sim_general_settings["min_investment_per_trade_percent"] = ui.min_investment_per_trade_percent.value()

    trade_sim_general_settings["investment_per_trade_decay_function"] = str(ui.investment_per_trade_decay_function.currentText())

    record_settings(trade_sim_general_settings, location, name="trade_sim_general_settings"+"_"+name)


def get_single_ticker_trade_sim_settings(ui, location="Current_settings", name=""):
    single_trade_sim_settings = {}

    # ___________________________ Metalabels parameters ______________________
    single_trade_sim_settings["run_metalabels"] = ui.run_metalabels.isChecked()

    single_trade_sim_settings["m_investment_settings"] = str(ui.m_investment_settings.currentText())
    single_trade_sim_settings["m_cash_in_settings"] = str(ui.m_cash_in_settings.currentText())

    # ___________________________ Stop-loss settings  ________________________
    # Max --> Min
    single_trade_sim_settings["max_prev_stop_loss"] = ui.max_prev_stop_loss.value()
    single_trade_sim_settings["min_prev_stop_loss"] = ui.min_prev_stop_loss.value()

    single_trade_sim_settings["prev_stop_loss_decay_function"] = str(ui.prev_stop_loss_decay_function.currentText())

    # Max --> Min
    single_trade_sim_settings["max_max_stop_loss"] = ui.max_max_stop_loss.value()
    single_trade_sim_settings["min_max_stop_loss"] = ui.min_max_stop_loss.value()

    single_trade_sim_settings["max_stop_loss_decay_function"] = str(ui.max_stop_loss_decay_function.currentText())

    record_settings(single_trade_sim_settings, location, name="single_trade_sim_settings"+"_"+name)


def get_multi_ticker_trade_sim_settings(ui, location="Current_settings", name=""):
    multi_trade_sim_settings = {}
    # ___________________________ Stop-loss settings  ________________________
    # Account
    # Max --> Min
    multi_trade_sim_settings["max_account_prev_stop_loss"] = ui.max_account_prev_stop_loss.value()
    multi_trade_sim_settings["min_account_prev_stop_loss"] = ui.min_account_prev_stop_loss.value()

    multi_trade_sim_settings["account_prev_stop_loss_decay_function"] = str(ui.account_prev_stop_loss_decay_function.currentText())

    # Max --> Min
    multi_trade_sim_settings["max_account_max_stop_loss"] = ui.max_account_max_stop_loss.value()
    multi_trade_sim_settings["min_account_max_stop_loss"] = ui.min_account_max_stop_loss.value()

    multi_trade_sim_settings["account_max_stop_loss_decay_function"] = str(ui.account_max_stop_loss_decay_function.currentText())

    # Ticker
    # Max --> Min
    multi_trade_sim_settings["max_ticker_prev_stop_loss"] = ui.max_ticker_prev_stop_loss.value()
    multi_trade_sim_settings["min_ticker_prev_stop_loss"] = ui.min_ticker_prev_stop_loss.value()

    multi_trade_sim_settings["ticker_prev_stop_loss_decay_function"] = str(ui.ticker_prev_stop_loss_decay_function.currentText())

    # Max --> Min
    multi_trade_sim_settings["max_ticker_max_stop_loss"] = ui.max_ticker_max_stop_loss.value()
    multi_trade_sim_settings["min_ticker_max_stop_loss"] = ui.min_ticker_max_stop_loss.value()

    multi_trade_sim_settings["ticker_max_stop_loss_decay_function"] = str(ui.ticker_max_stop_loss_decay_function.currentText())

    record_settings(multi_trade_sim_settings, location, name="multi_trade_sim_settings"+"_"+name)
