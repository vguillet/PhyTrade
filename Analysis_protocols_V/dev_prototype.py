from PhyTrade.Technical_Analysis.Data_Collection_preparation.Big_Data import BIGDATA
from PhyTrade.Technical_Analysis.Data_Collection_preparation.Yahoo import pull_yahoo_data

from PhyTrade.Technical_Analysis.Amplification_factors.Volatility_gen import VOLATILITY

from PhyTrade.Technical_Analysis.Tools.OC_gen import OC
from PhyTrade.Technical_Analysis.Tools.SPLINE_gen import SPLINE


class dev_prototype:
    def __init__(self):

        # ========================= DATA COLLECTION INITIALISATION =======================
        ticker = 'AAPL'                     # Ticker selected for Yahoo data collection
        data = pull_yahoo_data(ticker)      # Pull data from Yahoo

        # ========================= ANALYSIS INITIALISATION ==============================
        data_slice_start_ind = -200
        data_slice_stop_ind = len(data)

        self.big_data = BIGDATA(data, ticker, data_slice_start_ind, data_slice_stop_ind)
        # ------------------ Tools initialisation
        self.oc_tools = OC()
        self.spline_tools = SPLINE(self.big_data)

        # ------------------ Indicators initialisation
        setattr(self.big_data, "volatility", VOLATILITY(self.big_data))
        self.big_data.volatility.get_output(self.big_data)

        self.big_data.volatility.plot_volatility(self.big_data)
