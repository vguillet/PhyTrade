
"""
Used to generate metalabels using
"""

# Built-in/Generic Imports

# Libs

# Own modules
from PhyTrade.Settings.SETTINGS import SETTINGS
from PhyTrade.Data_Collection_preparation.Fetch_technical_data import fetch_technical_data
from PhyTrade.Tools.Trading_dataslice import Trading_dataslice

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


class Metalabeling_gen:
    def __init__(self, ticker, slice_size, metalabeling_method=0):
        # ---- Generate settings
        self.settings = SETTINGS(market_settings=True, metalabeling_settings=True)

        self.settings.metalabeling_settings.subslice_start_date = fetch_technical_data(ticker)["Date"][0]
        self.settings.metalabeling_settings.end_date = None
        self.settings.metalabeling_settings.data_slice_size = slice_size
        self.settings.metalabeling_settings.config_name = "Metalabels"
        self.data_slice = Trading_dataslice(ticker,
                                            self.settings.metalabeling_settings.subslice_start_date, self.settings.metalabeling_settings.data_slice_size,
                                            0, )

        if metalabeling_method == 0:
            self.settings.metalabeling_settings.gen_metalabels_settings()

        elif metalabeling_method == 1:
            self.settings.metalabeling_settings.gen_evoa_metalabels_settings()

            # --> Setup default parameters
            self.settings.metalabeling_settings.exploitation_phase_len = 0
            self.settings.metalabeling_settings.data_slice_shift_per_gen = self.settings.metalabeling_settings.data_slice_size
            self.settings.metalabeling_settings.data_slice_cycle_count = self.settings.metalabeling_settings.nb_of_generations
            self.settings.metalabeling_settings.data_looper = False
            self.settings.metalabeling_settings.starting_parameters = None

        # ---- Fetch data to metalabel


if __name__ == "__main__":
    metalabels = Metalabeling_gen("AAPL", 24, metalabeling_method=0)
