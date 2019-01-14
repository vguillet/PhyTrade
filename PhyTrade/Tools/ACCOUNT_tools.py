

class ACCOUNT:
    def __init__(self, initial_funds=1000):

        self.initial_funds = initial_funds

        self.current_funds = initial_funds
        self.current_assets = 0
        
        self.funds_history = []
        self.assets_history = []
        self.net_worth_history = []

    def convert_funds_to_assets(self, current_value, investment_per_trade):

        self.current_funds = self.current_funds - investment_per_trade
        self.current_assets = self.current_assets + investment_per_trade / current_value

        self.funds_history.append(self.current_funds)
        self.assets_history.append(self.current_assets)
        self.net_worth_history.append(self.current_funds + self.current_assets * current_value)

    def convert_assets_to_funds(self, current_value, assets_sold_per_trade):
        self.current_funds = self.current_funds + assets_sold_per_trade * current_value
        self.current_assets = self.current_assets - assets_sold_per_trade

        self.funds_history.append(self.current_funds)
        self.assets_history.append(self.current_assets)
        self.net_worth_history.append(self.current_funds + self.current_assets * current_value)

    def record_net_worth(self, current_value):
        self.funds_history.append(self.current_funds)
        self.assets_history.append(self.current_assets)
        self.net_worth_history.append(self.current_funds + self.current_assets * current_value)

    def calc_net_worth(self, current_value):
        return self.current_funds+self.current_assets*current_value

    def calc_net_profit(self, current_value):
        return self.current_funds+self.current_assets*current_value-self.initial_funds

    def print_account_status(self, current_value):
        print("Money =", self.current_funds, "$")
        print("Share owned=", self.current_assets)
        print("Total asset value=", self.calc_net_worth(current_value), "$")

    def plot_net_worth(self, dates):
        import matplotlib.pyplot as plt

        plt.plot(dates, self.net_worth_history)

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("Net worth over time")
        plt.xlabel("Trade date")
        plt.ylabel("Net worth ($)")
