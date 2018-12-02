from Analysis_protocol_V.Prototype_1 import Prototype_1


class Trade_bot:
    def __init__(self):
        self.p1 = Prototype_1()
        self.p1.plot(plot_1=False, plot_2=False, plot_3=True)

        self.start_trade_money = 0
        self.money = 1000

        self.investment_per_trade = 200
        self.share_owned = 0

        # Define trade actions
        self.trade_actions = ["hold"]*len(self.p1.big_data.data_slice_dates)

        for i in self.p1.big_data.sell_trigger_dates:
            self.trade_actions[self.p1.big_data.data_slice_dates.index(i)] = "sell"

        for i in self.p1.big_data.buy_trigger_dates:
            self.trade_actions[self.p1.big_data.data_slice_dates.index(i)] = "buy"

        print("Sell count =", len(self.p1.big_data.sell_trigger_dates))
        print("Buy count =", len(self.p1.big_data.buy_trigger_dates))

        successful_trades = 0
        failed_trades = 0

        for i in range(len(self.trade_actions)):

            if not self.trade_actions[i] == "hold":
                if self.trade_actions[i] == "sell" and not self.share_owned == 0:
                    net = self.p1.big_data.data_slice_open_values[i] * self.share_owned
                    self.money += net
                    self.share_owned = 0

                    if self.money > self.start_trade_money:
                        successful_trades += 1

                        print("================> Day ", i)
                        print("Trade action:", self.trade_actions[i])
                        print("Money =", self.money)
                        print("Share owned=", self.share_owned)

                        print("Total asset value=",
                              self.money + self.p1.big_data.data_slice_open_values[i] * self.share_owned)
                        print("Trade successful")

                    else:
                        failed_trades += 1

                        print("================> Day ", i)
                        print("Trade action:", self.trade_actions[i])
                        print("Money =", self.money)
                        print("Share owned=", self.share_owned)

                        print("Total asset value=",
                              self.money + self.p1.big_data.data_slice_open_values[i] * self.share_owned)
                        print("Trade failed")

                if not self.money == 0 and self.trade_actions[i] == "buy":
                    investment = self.investment_per_trade / self.p1.big_data.data_slice_open_values[i]
                    self.start_trade_money = self.money
                    self.money -= self.investment_per_trade

                    self.share_owned += investment

                    print("----------------- Day ", i)
                    print("Trade action:", self.trade_actions[i])
                    print("Money =", self.money)
                    print("Share owned=", self.share_owned)

                    print("Total asset value=",
                          self.money + self.p1.big_data.data_slice_open_values[i] * self.share_owned)

        print("==============================")
        print("Successful trades:", successful_trades)
        print("Failed trades:", failed_trades)
        print("Net worth:", self.money + self.p1.big_data.data_slice_open_values[-1] * self.share_owned)
