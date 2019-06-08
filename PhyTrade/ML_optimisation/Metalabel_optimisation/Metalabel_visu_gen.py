from PhyTrade.ML_optimisation.Metalabel_optimisation.METALABELING_gen import MetaLabeling
from PhyTrade.Tools.DATA_SLICE_gen import data_slice
from PhyTrade.Trade_simulations.Trading_bots.Tradebot_v4 import Tradebot_v4
import numpy as np

N = 50
ticker = "AAPL"

data_slice = data_slice(ticker, "2000-01-01", 400, 0, 0, 0, 0, 0)
upper_barrier = np.linspace(0, 40, N)
lower_barrier = np.linspace(0, 40, N)
look_ahead = np.linspace(0, 50, N)

# print(list(data_slice.data_slice["Open"]))

results = []
for i in look_ahead:
    results.append(Tradebot_v4(list(data_slice.sliced_data["Open"]),
                   MetaLabeling(20, -20, round(i, 0), data_slice, metalabel_setting=0).metalabels,
                               cash_in_settings=1).account.net_worth_history[-1])

print(results)

import matplotlib.pyplot as plt

plt.plot(range(len(results)), results)
plt.show()

# xx, yy, zz = np.meshgrid(upper_barrier, lower_barrier, look_ahead)
#
# f = np.zeros_like(xx)
#
# for i in upper_barrier:
#     for j in lower_barrier:
#         for k in look_ahead:
#             f[i, j, k] = MetaLabeling("AAPL", i, j, k, data_slice.start_index, data_slice.stop_index)



