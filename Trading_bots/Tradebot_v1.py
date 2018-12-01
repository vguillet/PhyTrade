from Analysis_protocol_V.Prototype_1 import Prototype_1


class Trade_bot:
    def __init__(self):
        self.p1 = Prototype_1()
        self.p1.plot(plot_1=False, plot_2=False, plot_3=True)

        self.money = 1000
        self.investment_per_trade = 500
        self.share_owned = 0

        # Define trade actions
        self.trade_actions = ["hold"]*len(self.p1.big_data.data_slice_dates)

        for i in self.p1.big_data.sell_trigger_dates:
            self.trade_actions[self.p1.big_data.data_slice_dates.index(i)] = "sell"

        for i in self.p1.big_data.buy_trigger_dates:
            self.trade_actions[self.p1.big_data.data_slice_dates.index(i)] = "buy"

        print("Sell count =", len(self.p1.big_data.sell_trigger_dates))
        print("Buy count =", len(self.p1.big_data.buy_trigger_dates))
        print(len(self.trade_actions))
        print(self.trade_actions)

        successful_trades = 0
        failed_trades = 0

        for i in range(len(self.trade_actions)):

            if not self.trade_actions[i] == "hold":
                if not self.share_owned == 0 and self.trade_actions[i] == "sell":
                    net = self.p1.big_data.data_slice_open_values[i] * self.share_owned
                    self.money += net
                    self.share_owned = 0
                    if net > 0:
                        successful_trades += 1
                    else:
                        failed_trades += 1

                if not self.money == 0 and self.trade_actions[i] == "buy":
                    investment = self.investment_per_trade / self.p1.big_data.data_slice_open_values[i]
                    self.money -= self.investment_per_trade

                    self.share_owned += investment

                print("----------------- Day ", i)
                print("Trade action:", self.trade_actions[i])
                print("Money =", self.money)
                print("Share owned=", self.share_owned)

                print("Total asset value=", self.money + self.p1.big_data.data_slice_open_values[i] * self.share_owned)

        print("==============================")
        print("Successful trades:", successful_trades)
        print("Failed trades:", failed_trades)
        print("Profit:", self.money - 1000)
