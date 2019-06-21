import json


class Model_settings:
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
        self.threshold_setting = 2

        self.buffer_type = ["No buffer", "Fixed value buffer", "Google-trend based evolutive buffer"]
        self.buffer_setting = 1
        # TODO: Add to evoa algo
        self.buffer = 0.05