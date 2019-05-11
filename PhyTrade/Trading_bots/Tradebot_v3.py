"""
This Trade bot is optimised for the GA parameter optimisation

"""

from PhyTrade.Trading_bots.ACCOUNT_tools import ACCOUNT
import matplotlib.pyplot as plt


class Tradebot_v3:
    def __init__(self, analysis,
                 investment_settings=1, cash_in_settings=0, stop_loss=0.94):

        # ============================ TRADE_BOT ATTRIBUTES ============================
        print_trade_process = False

        # -- Tradebot finance
        self.account = ACCOUNT(initial_funds=1000)
        self.stop_loss = stop_loss
        stop_loss_count = 0

        # -- Market analysis protocol
        self.analysis = analysis

        # -- Generate trade actions from analysis
        self.trade_actions = ["hold"] * len(self.analysis.big_data.data_slice_dates)

        if analysis.big_data.buy_sell_labels is None:
            for i in self.analysis.big_data.Major_spline.sell_dates:
                self.trade_actions[self.analysis.big_data.data_slice_dates.index(i)] = "sell"

            for i in self.analysis.big_data.Major_spline.buy_dates:
                self.trade_actions[self.analysis.big_data.data_slice_dates.index(i)] = "buy"

        else:
            for i in range(len(analysis.big_data.buy_sell_labels)):
                if analysis.big_data.buy_sell_labels[i] == 1:
                    self.trade_actions[i] = "sell"

                elif analysis.big_data.buy_sell_labels[i] == -1:
                    self.trade_actions[i] = "buy"

        # ==============================================================================
        """




        """
        # ============================ TRADE PROTOCOL DEF ==============================
        for i in range(len(self.trade_actions)):
            if print_trade_process:
                print("----------------- Day ", i)

            # ~~~~~~~~~~~~~~~~~~ Define the investment per trade
            if investment_settings == 0:
                if self.account.current_funds >= 100:
                    investment_per_trade = 100
                else:
                    investment_per_trade = self.account.current_funds

            elif investment_settings == 1:
                investment_per_trade = self.account.current_funds * 0.3

            # ~~~~~~~~~~~~~~~~~~ Define the assets sold per trade
            if cash_in_settings == 0:
                assets_sold_per_trade = self.account.current_assets

            elif cash_in_settings == 1:
                assets_sold_per_trade = self.account.current_assets * 0.3

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

                if print_trade_process:
                    print("==========================================================")
                    print("Stop-loss triggered")
                    self.account.print_account_status(self.analysis.big_data.data_slice_open_values[i])
                    print("==========================================================")

            # -- Define hold action
            elif self.trade_actions[i] == "hold":
                self.account.record_net_worth(self.analysis.big_data.data_slice_open_values[i])

                if print_trade_process:
                    print("->Hold")

            # -- Define buy action
            elif self.trade_actions[i] == "buy" and not self.account.current_funds == 0:
                self.account.convert_funds_to_assets(
                    self.analysis.big_data.data_slice_open_values[i], investment_per_trade)

                if print_trade_process:
                    print("Trade action: Buy")
                    print("Investment =", investment_per_trade, "$")
                    self.account.print_account_status(self.analysis.big_data.data_slice_open_values[i])

            # -- Define sell action
            elif self.trade_actions[i] == "sell" and not self.account.current_assets == 0:
                self.account.convert_assets_to_funds(
                    self.analysis.big_data.data_slice_open_values[i], assets_sold_per_trade)

                if print_trade_process:
                    print("Trade action: Sell")
                    print("Investment =", investment_per_trade, "$")
                    self.account.print_account_status(self.analysis.big_data.data_slice_open_values[i])

            else:
                self.account.record_net_worth(self.analysis.big_data.data_slice_open_values[i])

                if print_trade_process:
                    print("Trade action 'Sell' canceled because nothing to sell")

        # ==============================================================================
        """




        """
        # ============================ TRADE RESULTS/RECAP =============================
        if print_trade_process:
            print("")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Buy count =", len(self.analysis.big_data.Major_spline.buy_dates))
            print("Sell count =", len(self.analysis.big_data.Major_spline.sell_dates))
            print("Stop_loss_count =", stop_loss_count)
            print("")
            print("Net worth:", self.account.calc_net_worth(self.analysis.big_data.data_slice_open_values[-1]), "$")
            print("Profit=", self.account.calc_net_profit(self.analysis.big_data.data_slice_open_values[-1]))
            print("Percent profit=", self.account.calc_net_profit(self.analysis.big_data.data_slice_open_values[-1]) / 10)
            print("Max worth:", max(self.account.net_worth_history))
            print("Min worth:", min(self.account.net_worth_history))

            print("")
            print("1000$ simple initial investment:",
                  (1000 / self.analysis.big_data.data_slice_open_values[0]) * self.analysis.big_data.data_slice_open_values[
                      -1])
            self.account.plot_net_worth(self.analysis.big_data.data_slice_dates)
            plt.show()
