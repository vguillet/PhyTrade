from PhyTrade.Settings.Metalabeling_settings import Metalabeling_settings


class Metalabeling_gen:
    def __init__(self, ticker, metalabeling_method=0):
        metalabeling_settings = Metalabeling_settings()

        if metalabeling_method == 0:
            metalabeling_settings.gen_metalabels_settings()

        elif metalabeling_method == 1:
            metalabeling_settings.gen_evoa_metalabels_settings()
            metalabeling_settings.config_name = "Metalabels"

            # --> Setup default parameters
            metalabeling_settings.ticker = ticker
            metalabeling_settings.exploitation_phase_len = 0
            metalabeling_settings.data_slice_shift_per_gen = metalabeling_settings.data_slice_size
