from PhyTrade.Settings.Benchmark_settings import Benchmark_settings
from PhyTrade.Settings.Individual_settings import Individual_settings
from PhyTrade.Settings.Market_settings import Market_settings
from PhyTrade.Settings.Metalabeling_settings import Metalabeling_settings
from PhyTrade.Settings.Model_settings import Model_settings
from PhyTrade.Settings.Optimiser_settings import Optimiser_settings
from PhyTrade.Settings.Trade_sim_settings import Trade_sim_settings
from PhyTrade.Settings.Tradebot_settings import Tradebot_settings


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

