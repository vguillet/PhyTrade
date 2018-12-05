from Analysis_protocols_V.Prototype_1 import Prototype_1
from Analysis_protocols_V.Prototype_2 import Prototype_2


class Trade_bot_1:
    def __init__(self):

        # ============================ TRADE_BOT ATTRIBUTES ============================
        self.start_trade_money = 0
        self.money = 1000

        self.investment_per_trade = 0.6
        self.share_owned = 0

        # Market analysis protocol:

        # self.p = Prototype_1()
        # self.p.plot(plot_1=False, plot_2=False, plot_3=True)

        self.p = Prototype_2()
        self.p.plot(plot_1=False, plot_2=False, plot_3=True)

        # ==============================================================================
        """








        """
        # ============================ TRADE PROTOCOL DEF ==============================

        print("Buy count =", len(self.p.big_data.Major_spline.buy_dates))
        print("Sell count =", len(self.p.big_data.Major_spline.sell_dates))

        # Define trade actions
        self.trade_actions = ["hold"]*len(self.p.big_data.data_slice_dates)

        for i in self.p.big_data.Major_spline.sell_dates:
            self.trade_actions[self.p.big_data.data_slice_dates.index(i)] = "sell"

        for i in self.p.big_data.Major_spline.buy_dates:
            self.trade_actions[self.p.big_data.data_slice_dates.index(i)] = "buy"

        successful_trades = 0
        failed_trades = 0

        for i in range(len(self.trade_actions)):

            if self.money > 0:
                investment_per_trade = self.money * self.investment_per_trade
            else:
                investment_per_trade = 0

            if not self.trade_actions[i] == "hold":
                if self.trade_actions[i] == "sell" and not self.share_owned == 0:
                    net = self.p.big_data.data_slice_open_values[i] * self.share_owned
                    self.money += net
                    self.share_owned = 0

                    if self.money > self.start_trade_money:
                        successful_trades += 1

                        print("=====================================> Day ", i+1)
                        print("Trade action:", self.trade_actions[i])
                        print("Money =", self.money, "$")
                        print("Share owned=", self.share_owned)

                        print("Total asset value=",
                              self.money + self.p.big_data.data_slice_open_values[i] * self.share_owned)
                        print("Trade successful")

                    else:
                        failed_trades += 1

                        print("=====================================> Day ", i)
                        print("Trade action:", self.trade_actions[i])
                        print("Money =", self.money, "$")
                        print("Share owned=", self.share_owned)

                        print("Total asset value=",
                              self.money + self.p.big_data.data_slice_open_values[i] * self.share_owned, "$")
                        print("Trade failed")

                if not self.money == 0 and self.trade_actions[i] == "buy":
                    investment = investment_per_trade / self.p.big_data.data_slice_open_values[i]
                    self.start_trade_money = self.money
                    self.money -= investment_per_trade

                    self.share_owned += investment

                    print("----------------- Day ", i)
                    print("Trade action:", self.trade_actions[i])
                    print("Investment =", investment_per_trade, "$")
                    print("Money =", self.money, "$")
                    print("Share owned=", self.share_owned)

                    print("Total asset value=",
                          self.money + self.p.big_data.data_slice_open_values[i] * self.share_owned, "$")

        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Successful trades:", successful_trades)
        print("Failed trades:", failed_trades)
        print("")
        print("Net worth:", self.money + self.p.big_data.data_slice_open_values[-1] * self.share_owned, "$")
        print("Profit=", self.money + self.p.big_data.data_slice_open_values[-1] * self.share_owned - 1000)
