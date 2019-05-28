"""
Contains information about a Tradebot's account, along with it's transaction history etc...
"""


class ACCOUNT:
    def __init__(self, initial_funds=1000, initial_assets=0):
        """
        Stores the states of a trading account. Stores account history in:
            -> funds_history

            -> assets_history

            -> net_worth_history

        Contains the convert funds-to-assets and convert assets-to-funds methods to perform transactions

        :param initial_funds: Initial funds in the account
        :param initial_assets: Initial assets in the account (in number of stocks)
        """

        self.initial_funds = initial_funds
        self.initial_assets = initial_assets

        self.current_funds = initial_funds
        self.current_assets = initial_assets
        
        self.funds_history = []
        self.assets_history = []
        self.net_worth_history = []

    def convert_funds_to_assets(self, current_value, investment_per_trade):
        """
        Used to perform buy operations

        :param current_value: Current value of the stock brought
        :param investment_per_trade: Amount of investment to be performed
        """

        self.current_funds = self.current_funds - investment_per_trade
        self.current_assets = self.current_assets + investment_per_trade / current_value

        self.funds_history.append(self.current_funds)
        self.assets_history.append(self.current_assets)
        self.net_worth_history.append(self.current_funds + self.current_assets * current_value)

    def convert_assets_to_funds(self, current_value, assets_sold_per_trade):
        """
        Used to perform sell operation

        :param current_value: Current value of the stock sold
        :param assets_sold_per_trade: Amount of assets to be sold
        """
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
