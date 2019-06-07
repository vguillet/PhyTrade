from PhyTrade.ML_optimisation.Metalabel_optimisation.METALABELING_gen import MetaLabeling
from PhyTrade.Tools.DATA_SLICE_gen import data_slice
from PhyTrade.Trade_simulations.Trading_bots.Tradebot_v4 import Tradebot_v4
import numpy as np

N = 50
ticker = "AAPL"

data_slice = data_slice(ticker, "2000-01-01", 200, 0, 0, 0, 0, 0)
upper_barrier = np.linspace(0, 40, N)
lower_barrier = np.linspace(0, 1, N)
look_ahead = np.linspace(0, 1, N)

tradebot = Tradebot_v4()
# xx, yy, zz = np.meshgrid(upper_barrier, lower_barrier, look_ahead)
#
# f = np.zeros_like(xx)
#
# for i in upper_barrier:
#     for j in lower_barrier:
#         for k in look_ahead:
#             f[i, j, k] = MetaLabeling("AAPL", i, j, k, data_slice.start_index, data_slice.stop_index)



