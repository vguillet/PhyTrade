
##################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs
from PyQt5 import QtWidgets, QtGui, QtCore

# Own modules
from GUI_1_1.Tools.Settings_to_json import record_settings

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

##################################################################################################################


def gen_trade_sim_general_settings(ui):
    trade_sim_general_settings = {}

    # ___________________________ Simulation parameters ______________________
    trade_sim_general_settings["simulation_name"] = str(ui.simulation_name.currentText())
    trade_sim_general_settings["nb_data_slices"] = ui.nb_data_slices.value()

    # ___________________________ Print/plot parameters ______________________
    trade_sim_general_settings["print_trade_process"] = ui.print_trade_process.isChecked()
    trade_sim_general_settings["plot_eco_model_results"] = ui.plot_eco_model_results.isChecked()

    # ___________________________ Investment settings ________________________
    trade_sim_general_settings["investment_settings"] = str(ui.investment_settings.currentText())
    trade_sim_general_settings["cash_in_settings"] = str(ui.cash_in_settings.currentText())

    trade_sim_general_settings["initial_investment"] = ui.initial_investment

    # Max --> Min
    trade_sim_general_settings["max_investment_per_trade_percent"] = ui.max_investment_per_trade_percent
    trade_sim_general_settings["min_investment_per_trade_percent"] = ui.min_investment_per_trade_percent

    trade_sim_general_settings["investment_per_trade_decay_function"] = ui.investment_per_trade_decay_function


def gen_single_trade_sim_settings(ui):
    single_trade_sim_settings = {}

    # ___________________________ Metalabels parameters ______________________
    single_trade_sim_settings["run_metalabels"] = ui.run_metalabels

    single_trade_sim_settings["m_investment_settings"] = ui.m_investment_settings
    single_trade_sim_settings["m_cash_in_settings"] = ui.m_cash_in_settings

    # ___________________________ Stop-loss settings  ________________________
    # Max --> Min
    single_trade_sim_settings["max_prev_stop_loss"] = ui.max_prev_stop_loss
    single_trade_sim_settings["min_prev_stop_loss"] = ui.min_prev_stop_loss

    single_trade_sim_settings["prev_stop_loss_decay_function"] = ui.prev_stop_loss_decay_function

    # Max --> Min
    single_trade_sim_settings["max_max_stop_loss"] = ui.max_max_stop_loss
    single_trade_sim_settings["min_max_stop_loss"] = ui.min_max_stop_loss

    single_trade_sim_settings["max_stop_loss_decay_function"] = ui.max_stop_loss_decay_function


def gen_multi_trade_sim_settings(ui):
    multi_trade_sim_settings = {}
    # ___________________________ Stop-loss settings  ________________________
    # Account
    # Max --> Min
    multi_trade_sim_settings["max_account_prev_stop_loss"] = ui.max_account_prev_stop_loss
    multi_trade_sim_settings["min_account_prev_stop_loss"] = ui.min_account_prev_stop_loss

    multi_trade_sim_settings["account_prev_stop_loss_decay_function"] = ui.account_prev_stop_loss_decay_function

    # Max --> Min
    multi_trade_sim_settings["max_account_max_stop_loss"] = ui.max_account_max_stop_loss
    multi_trade_sim_settings["min_account_max_stop_loss"] = ui.min_account_max_stop_loss

    multi_trade_sim_settings["account_max_stop_loss_decay_function"] = ui.account_max_stop_loss_decay_function

    # Ticker
    # Max --> Min
    multi_trade_sim_settings["max_ticker_prev_stop_loss"] = ui.max_ticker_prev_stop_loss
    multi_trade_sim_settings["min_ticker_prev_stop_loss"] = ui.min_ticker_prev_stop_loss

    multi_trade_sim_settings["ticker_prev_stop_loss_decay_function"] = ui.ticker_prev_stop_loss_decay_function

    # Max --> Min
    multi_trade_sim_settings["max_ticker_max_stop_loss"] = ui.max_ticker_max_stop_loss
    multi_trade_sim_settings["min_ticker_max_stop_loss"] = ui.min_ticker_max_stop_loss

    multi_trade_sim_settings["ticker_max_stop_loss_decay_function"] = ui.ticker_max_stop_loss_decay_function