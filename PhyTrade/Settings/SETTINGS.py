
##################################################################################################################
"""
Used to combine all setting classes
"""

# Own modules
from PhyTrade.Settings.Benchmark_settings import Benchmark_settings
from PhyTrade.Settings.Individual_settings import Individual_settings
from PhyTrade.Settings.Market_settings import Market_settings
from PhyTrade.Settings.Metalabeling_settings import Metalabeling_settings
from PhyTrade.Settings.Model_settings import Model_settings
from PhyTrade.Settings.Optimiser_settings import Optimiser_settings
from PhyTrade.Settings.Trade_sim_settings import Trade_sim_settings
from PhyTrade.Settings.Tradebot_settings import Tradebot_settings

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class SETTINGS:
    def __init__(self):
            self.benchmark_settings = Benchmark_settings()
            self.individual_settings = Individual_settings()
            self.market_settings = Market_settings()
            self.metalabeling_settings = Metalabeling_settings()
            self.model_settings = Model_settings()
            self.signal_training_settings = Optimiser_settings()
            self.trade_sim_settings = Trade_sim_settings()
            self.tradebot_settings = Tradebot_settings()

    def fetch_dates(self, setting):
            self.market_settings.gen_market_settings()

            # --> Training dates
            if setting == 1:
                self.start_date = self.market_settings.training_start_date
                self.end_date = self.market_settings.training_end_date

            # --> EVOA Metalabels dates
            elif setting == 2:
                self.start_date = self.market_settings.training_start_date
                self.end_date = self.market_settings.testing_end_date

            # --> Testing dates
            else:
                self.start_date = self.market_settings.testing_start_date
                self.end_date = self.market_settings.testing_end_date
