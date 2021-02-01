
##################################################################################################################
"""
Contain settings used for running trade simulations
"""

# Built-in/Generic Imports
import json

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class Trade_sim_settings:
    general_trade_sim_settings = json.load(open(r"C:\Users\Victor Guillet\Google Drive\Computer science\2-Programing\Repos\Python\Steffegium\Data\Settings\Current_settings\trade_sim_general_settings_.json"))

    decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
    investment_settings = ["Fixed investment value", "Fixed investment percentage", "Investment value pegged to trade signal",
                           "Investment percentage pegged to trade signal"]
    cash_in_settings = ["Total asset liquidation", "Fixed liquidation percentage", "Liquidation percentage pegged to trade signal"]

    # ___________________________ Simulation parameters ______________________
    simulation_name = general_trade_sim_settings["simulation_name"]
    nb_data_slices = general_trade_sim_settings["nb_data_slices"]

    # ___________________________ Print/plot parameters ______________________
    plot_eco_model_results = general_trade_sim_settings["plot_eco_model_results_sim"]
    print_trade_process = general_trade_sim_settings["print_trade_process"]

    # ___________________________ Investment settings ________________________

    investment_settings = investment_settings.index(general_trade_sim_settings["investment_settings"])
    cash_in_settings = cash_in_settings.index(general_trade_sim_settings["cash_in_settings"])

    # Max --> Min
    max_investment_per_trade_percent = general_trade_sim_settings["max_investment_per_trade_percent"]
    min_investment_per_trade_percent = general_trade_sim_settings["min_investment_per_trade_percent"]

    investment_per_trade_decay_function = decay_functions.index(general_trade_sim_settings["investment_per_trade_decay_function"])

    # =============================== SINGLE TRADE SIM SETTINGS ===================
    def gen_single_trade_sim(self):
        single_ticker_trade_sim_settings = json.load(open(r"C:\Users\Victor Guillet\Google Drive\Computer science\2-Programing\Repos\Python\Steffegium\Data\Settings\Current_settings\single_trade_sim_settings_.json"))

        investment_settings = ["Fixed investment value", "Fixed investment percentage", "Investment value pegged to trade signal",
                               "Investment percentage pegged to trade signal"]
        cash_in_settings = ["Total asset liquidation", "Fixed liquidation percentage", "Liquidation percentage pegged to trade signal"]
        decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]

        # ___________________________ Metalabels parameters ______________________
        self.run_metalabels = single_ticker_trade_sim_settings["run_metalabels"]     # Can be switched off for performance increase

        self.m_investment_settings = investment_settings.index(single_ticker_trade_sim_settings["investment_settings"])
        self.m_cash_in_settings = cash_in_settings.index(single_ticker_trade_sim_settings["cash_in_settings"])

        # ___________________________ Stop-loss settings  ________________________
        # Max --> Min
        self.max_prev_stop_loss = single_ticker_trade_sim_settings["max_prev_stop_loss"]
        self.min_prev_stop_loss = single_ticker_trade_sim_settings["min_prev_stop_loss"]

        self.prev_stop_loss_decay_function = decay_functions.index(single_ticker_trade_sim_settings["prev_stop_loss_decay_function"])

        # Max --> Min
        self.max_max_stop_loss = single_ticker_trade_sim_settings["max_max_stop_loss"]
        self.min_max_stop_loss = single_ticker_trade_sim_settings["min_max_stop_loss"]

        self.max_stop_loss_decay_function = decay_functions.index(single_ticker_trade_sim_settings["investment_settings"])

    # =============================== MULTI TRADE SIM SETTINGS ====================
    def gen_multi_trade_sim(self):
        multi_ticker_trade_sim_settings = json.load(open(r"C:\Users\Victor Guillet\Google Drive\Computer science\2-Programing\Repos\Python\Steffegium\Data\Settings\Current_settings\multi_trade_sim_settings_.json"))

        decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        # ___________________________ Stop-loss settings  ________________________
        # Account
        # Max --> Min
        self.max_account_prev_stop_loss = multi_ticker_trade_sim_settings["max_account_prev_stop_loss"]
        self.min_account_prev_stop_loss = multi_ticker_trade_sim_settings["min_account_prev_stop_loss"]

        self.account_prev_stop_loss_decay_function = decay_functions.index(multi_ticker_trade_sim_settings["account_prev_stop_loss_decay_function"])

        # Max --> Min
        self.max_account_max_stop_loss = multi_ticker_trade_sim_settings["max_account_max_stop_loss"]
        self.min_account_max_stop_loss = multi_ticker_trade_sim_settings["min_account_max_stop_loss"]

        self.account_max_stop_loss_decay_function = decay_functions.index(multi_ticker_trade_sim_settings["account_max_stop_loss_decay_function"])

        # Ticker
        # Max --> Min
        self.max_ticker_prev_stop_loss = multi_ticker_trade_sim_settings["max_ticker_prev_stop_loss"]
        self.min_ticker_prev_stop_loss = multi_ticker_trade_sim_settings["min_ticker_prev_stop_loss"]

        self.ticker_prev_stop_loss_decay_function = decay_functions.index(multi_ticker_trade_sim_settings["ticker_prev_stop_loss_decay_function"])

        # Max --> Min
        self.max_ticker_max_stop_loss = multi_ticker_trade_sim_settings["max_ticker_max_stop_loss"]
        self.min_ticker_max_stop_loss = multi_ticker_trade_sim_settings["min_ticker_max_stop_loss"]

        self.ticker_max_stop_loss_decay_function = decay_functions.index(multi_ticker_trade_sim_settings["ticker_max_stop_loss_decay_function"])
