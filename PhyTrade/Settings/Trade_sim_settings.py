import json


class Trade_sim_settings:
    # =============================== SINGLE TRADE SIM SETTINGS ===================
    def gen_single_trade_sim(self):
        # ___________________________ Simulation parameters ______________________
        self.simulation_name = "1"
        self.nb_data_slices = 100

        # ___________________________ Print/plot parameters ______________________
        self.plot_eco_model_results = False
        self.print_trade_process = False

        # ___________________________ Metalabels parameters ______________________
        self.run_metalabels = False     # Can be switched off for performance increase

        self.m_investment_settings = 1
        self.m_cash_in_settings = 0

        # ___________________________ Investment settings ________________________
        self.investment_settings = 3
        self.cash_in_settings = 2

        self.max_investment_per_trade_percent = 0.3
        self.min_investment_per_trade_percent = 0.01

        self.investment_per_trade_decay_function = 1

        # ___________________________ Stop-loss settings  ________________________
        # Max --> Min
        self.max_prev_stop_loss = 0.85
        self.min_prev_stop_loss = 0.98

        self.prev_stop_loss_decay_function = 1

        # Max --> Min
        self.max_max_stop_loss = 0.75
        self.min_max_stop_loss = 0.95

        self.max_stop_loss_decay_function = 1

    # =============================== MULTI TRADE SIM SETTINGS ====================
    def gen_multi_trade_sim(self):
        # ___________________________ Simulation parameters ______________________
        self.simulation_name = "1"
        self.nb_data_slices = 50

        # ___________________________ Print/plot parameters ______________________
        self.plot_eco_model_results = True
        self.print_trade_process = False

        # ___________________________ Investment settings ________________________
        self.investment_settings = 3
        self.cash_in_settings = 2

        self.initial_investment = 1000

        # Max --> Min
        self.max_investment_per_trade_percent = 0.1
        self.min_investment_per_trade_percent = 0.000001

        self.investment_per_trade_decay_function = 1

        # ___________________________ Stop-loss settings  ________________________
        # Account
        # Max --> Min
        self.max_account_prev_stop_loss = 0.85
        self.min_account_prev_stop_loss = 0.98

        self.account_prev_stop_loss_decay_function = 1

        # Max --> Min
        self.max_account_max_stop_loss = 0.75
        self.min_account_max_stop_loss = 0.95

        self.account_max_stop_loss_decay_function = 1

        # Ticker
        # Max --> Min
        self.max_ticker_prev_stop_loss = 0.80
        self.min_ticker_prev_stop_loss = 0.98

        self.ticker_prev_stop_loss_decay_function = 1

        # Max --> Min
        self.max_ticker_max_stop_loss = 0.70
        self.min_ticker_max_stop_loss = 0.95

        self.ticker_max_stop_loss_decay_function = 1
