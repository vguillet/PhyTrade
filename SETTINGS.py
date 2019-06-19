import multiprocessing
import json


class SETTINGS:
    # =============================== ECONOMIC MODEL SETTINGS =====================
    def gen_model_settings(self):
        self.spline_interpolation_factor = 4

        # ___________________________ RSI parameters _____________________________
        self.rsi_buffer_setting = 0
        self.rsi_include_triggers_in_bb_signal = True

        # ___________________________ SMA parameters _____________________________
        self.sma_include_triggers_in_bb_signal = False

        # ___________________________ EMA parameters _____________________________
        self.ema_include_triggers_in_bb_signal = False

        # ___________________________ LWMA parameters ____________________________
        self.lwma_include_triggers_in_bb_signal = False

        # ___________________________ CCI parameters ____________________________
        self.cci_include_triggers_in_bb_signal = False

        # ___________________________ OC_GRADIENT parameters ____________________________
        self.oc_gradient_include_triggers_in_bb_signal = False

        # ___________________________ Modulation parameters ______________________
        # TODO: Add to evoa algo
        self.volume_std_dev_max = 3
        self.volatility_std_dev_max = 3

        # ___________________________ Threshold parameters _______________________
        self.threshold_type = ["Fixed value", "Bollinger bands size", "Bollinger bands/price diff"]
        self.threshold_setting = 1

        self.buffer_type = ["No buffer", "Fixed value buffer", "Google-trend based evolutive buffer"]
        self.buffer_setting = 1
        # TODO: Add to evoa algo
        self.buffer = 0.05

    # =============================== INDIVIDUAL GEN SETTINGS =====================
    def gen_individual_settings(self):
        self.rsi_count = 2
        self.sma_count = 2
        self.ema_count = 4
        self.lwma_count = 0
        self.cci_count = 3
        self.eom_count = 2

    # =============================== SINGLE TRADE SIM SETTINGS ===================
    def gen_run_model_settings(self):
        self.print_trade_process = False

        # ___________________________ Model parameters ___________________________
        self.evaluation_name = "1"

        self.ticker = "AAPL"
        self.parameter_set = json.load(open(r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Parameter_sets\Run_4_AAPL.json".replace('\\', '/')))
        # self.parameter_set = None

        self.start_date = "2018-01-02"
        self.data_slice_size = 200

        # ___________________________ Metalabels parameters ______________________
        self.gen_metalabels_settings()

    # =============================== EVOA SETTINGS ===============================
    def gen_evoa_settings(self):
        # ___________________________ Optimisation parameters ____________________
        self.config_name = "Run_5"

        self.tickers = ["AAPL", "INTC", "NVDA", "SSNLF"]
        # self.tickers = ["AAPL"]

        # ___________________________ Print/plot parameters ______________________
        self.print_evoa_parameters_per_gen = True
        self.print_evaluation_status = False

        self.plot_best_individual_eco_model_results = True
        self.plot_eco_model_results = False

        # ___________________________ EVO_algo main parameters ___________________
        self.population_size = 30
        self.nb_of_generations = 25

        self.mutation_rate = 0.5
        self.nb_parents = 7
        self.nb_random_ind = 3

        self.exploitation_phase_len_percent = 0.15
        self.exploitation_phase_len = round(self.nb_of_generations*self.exploitation_phase_len_percent)

        self.data_slice_start_date = "2017-01-03"
        self.data_slice_size = 200
        self.data_slice_shift_per_gen = 0
        self.data_slice_cycle_count = 10

        self.data_looper = False

        # TODO: Add slize size auto scaling according to generation count/cycle count and start/end date
        self.end_date = "2019-01-02"
        # self.end_date = None

        # ___________________________ Generation 0 parameters ____________________
        # -- Starting parameters
        # --> Set to None if random initial population wanted
        # self.starting_parameters = json.load(open(r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Parameter_sets\Run_4_AAPL.json".replace('\\', '/')))
        self.starting_parameters = None

        # -- Generations settings
        self.evaluation_methods = ["Profit", "MetaLabels", "MetaLabels bs", "MetaLabels avg", "Buy count", "Sell count", "Transaction count"]
        self.evaluation_method = 0

        self.decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        self.parents_decay_function = 1
        self.random_ind_decay_function = 1
        self.mutation_decay_function = 1

        self.parents_selection_methods = ["Elitic"]
        self.parents_selection_method = 0

        # -- max_worker_processes
        self.max_worker_processes = multiprocessing.cpu_count() - 1

        # ___________________________ Benchmark parameters _______________________
        # -- Benchmarking data slice settings
        self.benchmark_data_slice_start_date = "2019-01-02"
        self.benchmark_data_slice_size = 200

        # ___________________________ Metalabels parameters ______________________
        self.gen_metalabels_settings()

        self.gen_individual_settings()

    # =============================== METALABELING SETTINGS =======================
    def gen_metalabels_settings(self):
        # -- Metalabeling settings:
        self.metalabeling_settings = ["Peak", "Simple", "Hybrid"]
        self.metalabeling_setting = 0

        self.upper_barrier = 20
        self.lower_barrier = -20
        self.look_ahead = 20

    # =============================== TRADEBOT SETTINGS ===========================
    def gen_tradebot_settings(self):
        # --> Simple investment settings
        self.s_initial_investment = 1000

        # --> Investment settings
        self.fixed_investment = 100
        self.investment_percentage = 0.3

        self.asset_liquidation_percentage = 0.5

    # =============================== SINGLE TRADE SIM SETTINGS ===================
    def gen_single_trade_sim(self):
        # ___________________________ Simulation parameters ______________________
        self.simulation_name = "1"

        self.ticker = "AAPL"
        self.parameter_set = json.load(open(r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Parameter_sets\Run_2_AAPL.json".replace('\\', '/')))

        self.start_date = "2010-01-01"
        self.data_slice_size = 200
        self.nb_data_slices = 10

        # ___________________________ Print/plot parameters ______________________
        self.plot_eco_model_results = False
        self.print_trade_process = False

        # ___________________________ Metalabels parameters ______________________
        self.run_metalabels = False     # Can be switched off for performance increase
        self.gen_metalabels_settings()

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

        self.parameter_sets = []
        self.parameter_sets.append(json.load(open(
            r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Parameter_sets\Run_5_AAPL.json".replace(
                '\\', '/'))))
        self.parameter_sets.append(json.load(open(
            r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Parameter_sets\Run_5_NVDA.json".replace(
                '\\', '/'))))
        self.parameter_sets.append(json.load(open(
            r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Parameter_sets\Run_5_INTC.json".replace(
                '\\', '/'))))
        # self.parameter_sets.append(json.load(open(
        #     r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Parameter_sets\Run_5_AMZN.json".replace(
        #         '\\', '/'))))

        self.tickers = ["AAPL", "NVDA", "INTC"]
        # self.tickers = ["AAPL"]

        self.start_date = "2019-01-02"
        self.data_slice_size = 24
        self.nb_data_slices = 50

        # ___________________________ Print/plot parameters ______________________
        self.plot_eco_model_results = False
        self.print_trade_process = True

        # ___________________________ Metalabels parameters ______________________
        self.gen_metalabels_settings()

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
