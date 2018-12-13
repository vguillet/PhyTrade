from Analysis_protocols_V.Prototype_1 import Prototype_1
from Analysis_protocols_V.Prototype_2 import Prototype_2

from PhyTrade.Technical_Analysis.Tools.ACCOUNT_tools import ACCOUNT

import matplotlib.pyplot as plt


class Tradebot_v2:
    def __init__(self, investment_settings=1, stop_loss=0.95):

        # ============================ TRADE_BOT ATTRIBUTES ============================

        self.successful_trades = 0
        self.failed_trades = 0

        # -- Tradebot finance
        self.account = ACCOUNT(initial_funds=1000)
        self.stop_loss = stop_loss

        # -- Market analysis protocol
        # self.analysis = Prototype_1()
        # self.analysis.plot(plot_1=False, plot_2=False, plot_3=True)
        self.analysis = Prototype_2()
        self.analysis.plot(plot_1=False, plot_2=False, plot_3=True)

        # -- Generate trade actions from analysis
        self.trade_actions = ["hold"]*len(self.analysis.big_data.data_slice_dates)

        for i in self.analysis.big_data.Major_spline.sell_dates:
            self.trade_actions[self.analysis.big_data.data_slice_dates.index(i)] = "sell"

        for i in self.analysis.big_data.Major_spline.buy_dates:
            self.trade_actions[self.analysis.big_data.data_slice_dates.index(i)] = "buy"

        # ==============================================================================
        """




        """
        # ============================ TRADE PROTOCOL DEF ==============================
        for i in range(len(self.trade_actions)):
            print("----------------- Day ", i + 1)

            # ~~~~~~~~~~~~~~~~~~ Define the investment per trade
            if investment_settings == 0:
                investment_per_trade = 100

            elif investment_settings == 1:
                investment_per_trade = self.account.current_funds * 0.5
            """
            
            
            """
            # ~~~~~~~~~~~~~~~~~~ Define trade protocol
            # -- Define stop-loss
            if self.account.calc_net_worth(
                self.analysis.big_data.data_slice_open_values[i]) < \
                 max(self.account.net_worth_history) * self.stop_loss and not self.account.current_assets == 0:

                self.account.convert_assets_to_funds(
                    self.analysis.big_data.data_slice_open_values[i],
                    self.account.current_assets * self.analysis.big_data.data_slice_open_values[i])

                print("==========================================================")
                print("Stop-loss triggered")
                self.account.print_account_status(self.analysis.big_data.data_slice_open_values[i])
                print("==========================================================")

            # -- Define hold action
            elif self.trade_actions[i] == "hold":
                self.account.record_net_worth(self.analysis.big_data.data_slice_open_values[i])

            # -- Define buy action
            elif self.trade_actions[i] == "buy":
                self.account.convert_funds_to_assets(
                    self.analysis.big_data.data_slice_open_values[i], investment_per_trade)

                print("Trade action: Buy")
                print("Investment =", investment_per_trade, "$")
                self.account.print_account_status(self.analysis.big_data.data_slice_open_values[i])

            # -- Define sell action
            elif self.trade_actions[i] == "sell" and not self.account.current_assets == 0:
                self.account.convert_assets_to_funds(
                    self.analysis.big_data.data_slice_open_values[i], investment_per_trade)

                print("Trade action: Sell")
                print("Investment =", investment_per_trade, "$")
                self.account.print_account_status(self.analysis.big_data.data_slice_open_values[i])

        # ==============================================================================
        """




        """
        # ============================ TRADE RESULTS/RECAP =============================
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Buy count =", len(self.analysis.big_data.Major_spline.buy_dates))
        print("Sell count =", len(self.analysis.big_data.Major_spline.sell_dates))
        print("")
        print("Successful trades:", self.successful_trades)
        print("Failed trades:", self.failed_trades)
        print("")
        print("Net worth:", self.account.calc_net_worth(self.analysis.big_data.data_slice_open_values[-1]), "$")
        print("Profit=", self.account.calc_net_profit(self.analysis.big_data.data_slice_open_values[-1]))
        print("Percent profit=", self.account.calc_net_profit(self.analysis.big_data.data_slice_open_values[-1])/10)
        print("Max worth:", max(self.account.net_worth_history))
        print("Min worth:", min(self.account.net_worth_history))
        self.account.plot_net_worth(self.analysis.big_data.data_slice_dates)
        plt.show()










