import json


class Trade_sim_settings:
    # ___________________________ Simulation parameters ______________________
    simulation_name = "1"
    nb_data_slices = 5

    # ___________________________ Print/plot parameters ______________________
    plot_eco_model_results = False
    print_trade_process = False

    # ___________________________ Investment settings ________________________
    investment_settings = 3
    cash_in_settings = 2

    initial_investment = 1000

    # Max --> Min
    max_investment_per_trade_percent = 0.10
    min_investment_per_trade_percent = 0.05

    investment_per_trade_decay_function = 1

    # =============================== SINGLE TRADE SIM SETTINGS ===================
    def gen_single_trade_sim(self):

        # ___________________________ Metalabels parameters ______________________
        self.run_metalabels = True     # Can be switched off for performance increase

        self.m_investment_settings = 1
        self.m_cash_in_settings = 0

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
        # ___________________________ Stop-loss settings  ________________________
        # Account
        # Max --> Min
        self.max_account_prev_stop_loss = 0.90
        self.min_account_prev_stop_loss = 0.95

        self.account_prev_stop_loss_decay_function = 1

        # Max --> Min
        self.max_account_max_stop_loss = 0.85
        self.min_account_max_stop_loss = 0.95

        self.account_max_stop_loss_decay_function = 1

        # Ticker
        # Max --> Min
        self.max_ticker_prev_stop_loss = 0.85
        self.min_ticker_prev_stop_loss = 0.95

        self.ticker_prev_stop_loss_decay_function = 1

        # Max --> Min
        self.max_ticker_max_stop_loss = 0.85
        self.min_ticker_max_stop_loss = 0.95

        self.ticker_max_stop_loss_decay_function = 1
