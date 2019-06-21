from PhyTrade.ML_optimisation.Metalabel_optimisation.METALABELING_gen import MetaLabeling
from PhyTrade.Tools.DATA_SLICE_gen import data_slice
from PhyTrade.Trade_simulations.Trading_bots.Tradebot_v4 import Tradebot_v4
from PhyTrade.Tools.PLOT_tools import PLOT_tools
from pylab import *
import numpy as np

N = 40
ticker = "AAPL"

data_slice = data_slice(ticker, "2000-01-01", 400, 0, data_selection="Close")
# upper_barrier = np.linspace(1, 100, N)
# lower_barrier = np.linspace(1, 100, N)
# look_ahead = np.linspace(1, 200, N)

upper_barrier = 20
lower_barrier = -20
look_ahead = 20

metalabel_settings = 2

# --> Peak-dip metalabel visualisation
# print(MetaLabeling(20, -20, 10, data_slice, metalabel_setting=0).metalabels)
print(Tradebot_v4(list(data_slice.sliced_data_selection),
                  MetaLabeling(upper_barrier, lower_barrier, look_ahead, data_slice, metalabel_setting=metalabel_settings).metalabels,
                  cash_in_settings=0, print_trade_process=False).account.net_worth_history[-1])

plot_tools = PLOT_tools()

plot_tools.plot_oc_values(data_slice)
plot_tools.plot_values_trigger(data_slice, MetaLabeling(upper_barrier, lower_barrier, look_ahead, data_slice,
                                                        metalabel_setting=metalabel_settings).metalabels)

plt.show()

# print(MetaLabeling(20, -20, 10, data_slice, metalabel_setting=0).metalabels)
#
# plt.plot(range(len(results)), results)
# plt.show()

# --> Simple metalabel visualisation
# xx, yy, zz = np.meshgrid(upper_barrier, lower_barrier, look_ahead)
#
# f = np.zeros_like(xx)
#
# max_val = 0
# max_index = []
#
# for i in range(N):
#     for j in range(N):
#         for k in range(N):
#             h = Tradebot_v4(list(data_slice.sliced_data_selection),
#                             MetaLabeling(upper_barrier[i], lower_barrier[j], look_ahead[k], data_slice, metalabel_setting=1).metalabels,
#                             cash_in_settings=1).account.net_worth_history[-1]
#
#             if h > max_val:
#                 max_val = h
#                 max_index = [upper_barrier[i], lower_barrier[j], look_ahead[k]]
#                 print(max_val)
#
# print(max_val)
# print(max_index)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(f[:, 0], f[:, 1], f[:, 2])
#
# plt.show()
