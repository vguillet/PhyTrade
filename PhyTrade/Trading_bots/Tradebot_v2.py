from PhyTrade.Analysis_protocols_V.Prototype_2 import Prototype_2
from PhyTrade.Technical_Analysis.Tools.ACCOUNT_tools import ACCOUNT
import matplotlib.pyplot as plt


class Tradebot_v2:
    def __init__(self, investment_settings=1, cash_in_settings=0, stop_loss=0.92):

        # ============================ TRADE_BOT ATTRIBUTES ============================
        # -- Tradebot finance
        self.account = ACCOUNT(initial_funds=1000)
        self.stop_loss = stop_loss
        stop_loss_count = 0

        # -- Market analysis protocol
        self.analysis = Prototype_2()
        self.analysis.plot(plot_1=False, plot_2=False, plot_3=False)

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
            print("----------------- Day ", i)

            # ~~~~~~~~~~~~~~~~~~ Define the investment per trade
            if investment_settings == 0:
                if self.account.current_funds >= 100:
                    investment_per_trade = 100
                else:
                    investment_per_trade = self.account.current_funds

            elif investment_settings == 1:
                investment_per_trade = self.account.current_funds * 0.5

            # ~~~~~~~~~~~~~~~~~~ Define the assets sold per trade
            if cash_in_settings == 0:
                assets_sold_per_trade = self.account.current_assets

            elif cash_in_settings == 1:
                assets_sold_per_trade = self.account.current_assets*0.5

            # ~~~~~~~~~~~~~~~~~~ Define the variable stop-loss value
            if i % 100 == 0 and not self.stop_loss == 0.97:
                self.stop_loss += 0.01

            """
            
            
            """
            # ~~~~~~~~~~~~~~~~~~ Define trade protocol
            # -- Define stop-loss action
            if not len(self.account.net_worth_history) == 0 and \
                    self.account.calc_net_worth(self.analysis.big_data.data_slice_open_values[i]) < \
                    max(self.account.net_worth_history) * self.stop_loss and \
                    not self.account.current_assets == 0:

                self.account.convert_assets_to_funds(
                    self.analysis.big_data.data_slice_open_values[i],
                    self.account.current_assets)

                stop_loss_count += 1

                print("==========================================================")
                print("Stop-loss triggered")
                self.account.print_account_status(self.analysis.big_data.data_slice_open_values[i])
                print("==========================================================")

            # -- Define hold action
            elif self.trade_actions[i] == "hold":
                self.account.record_net_worth(self.analysis.big_data.data_slice_open_values[i])
                print("->Hold")

            # -- Define buy action
            elif self.trade_actions[i] == "buy" and not self.account.current_funds == 0:
                self.account.convert_funds_to_assets(
                    self.analysis.big_data.data_slice_open_values[i], investment_per_trade)

                print("Trade action: Buy")
                print("Investment =", investment_per_trade, "$")
                self.account.print_account_status(self.analysis.big_data.data_slice_open_values[i])

            # -- Define sell action
            elif self.trade_actions[i] == "sell" and not self.account.current_assets == 0:
                self.account.convert_assets_to_funds(
                    self.analysis.big_data.data_slice_open_values[i], assets_sold_per_trade)

                print("Trade action: Sell")
                print("Investment =", investment_per_trade, "$")
                self.account.print_account_status(self.analysis.big_data.data_slice_open_values[i])

            else:
                print("Trade action 'Sell' canceled because nothing to sell")
                self.account.record_net_worth(self.analysis.big_data.data_slice_open_values[i])

        # ==============================================================================
        """




        """
        # ============================ TRADE RESULTS/RECAP =============================
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Buy count =", len(self.analysis.big_data.Major_spline.buy_dates))
        print("Sell count =", len(self.analysis.big_data.Major_spline.sell_dates))
        print("Stop_loss_count =", stop_loss_count)
        print("")
        print("Net worth:", self.account.calc_net_worth(self.analysis.big_data.data_slice_open_values[-1]), "$")
        print("Profit=", self.account.calc_net_profit(self.analysis.big_data.data_slice_open_values[-1]))
        print("Percent profit=", self.account.calc_net_profit(self.analysis.big_data.data_slice_open_values[-1])/10)
        print("Max worth:", max(self.account.net_worth_history))
        print("Min worth:", min(self.account.net_worth_history))

        print("")
        print("1000$ simple initial investment:",
              (1000/self.analysis.big_data.data_slice_open_values[0])*self.analysis.big_data.data_slice_open_values[-1])
        self.account.plot_net_worth(self.analysis.big_data.data_slice_dates)
        plt.show()
