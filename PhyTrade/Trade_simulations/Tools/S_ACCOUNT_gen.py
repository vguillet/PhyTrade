"""
Contains information about a Tradebot's account, along with it's transaction history etc...
"""
from PhyTrade.Tools.MARKET_tools import MARKET_tools


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

        self.simple_investment_assets = None
        self.simple_investment_net_worth = []

    def convert_funds_to_assets(self, current_value, investment_per_trade):
        """
        Used to perform buy operations

        :param current_value: Current value of the stock brought
        :param investment_per_trade: Amount of investment to be performed
        """

        # --> Calculate transaction cost
        self.current_funds -= MARKET_tools().calc_transaction_cost(investment_per_trade/current_value)

        # --> Create order
        self.current_funds -= investment_per_trade
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

        # --> Calculate transaction cost
        # --> Calculate transaction cost
        self.current_funds -= MARKET_tools().calc_transaction_cost(assets_sold_per_trade/current_value)

        self.current_funds += assets_sold_per_trade * current_value
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

    def start_simple_investment(self, current_value, initial_investment=1000):
        self.simple_investment_assets = initial_investment/current_value

    def calc_simple_investment_value(self, current_value):
        self.simple_investment_net_worth.append(self.simple_investment_assets*current_value)

    def print_account_status(self, current_value):
        print("Current funds =", round(self.current_funds), "$")
        print("Share owned=", round(self.current_assets))
        print("Total net worth=", round(self.calc_net_worth(current_value)), "$")
        print("")

    def plot_net_worth(self, dates):
        import matplotlib.pyplot as plt

        plt.plot(dates, self.net_worth_history, label="Net worth history")
        plt.plot(dates, self.simple_investment_net_worth, label="Simple investment net worth")

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.legend()
        plt.title("Net worth over time")
        plt.xlabel("Trade date")
        plt.ylabel("Net worth ($)")
        plt.show()
