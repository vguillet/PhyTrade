"""
Contains information about a Tradebot's account, along with it's transaction history etc...
"""
from PhyTrade.Trade_simulations.Tools.ORDER_gen import ORDER_gen


class ACCOUNT:
    def __init__(self, initial_funds=1000, initial_orders=[]):
        """
        Stores the states of a trading account. Stores account history in:
            -> funds_history

            -> assets_history

            -> net_worth_history

        Contains the convert funds-to-assets and convert assets-to-funds methods to perform transactions
        The update_account must be run for each new day to allow for a correct updating of the orders

        :param initial_funds: Initial funds in the account
        :param initial_orders: Initial orders in the account (as order class instances)
        """

        # ---- Account initialisation
        self.initial_funds = initial_funds
        self.initial_orders = initial_orders

        # ---- Records initialisation
        # --> Record initial orders in content
        self.content = {}
        for order in self.initial_orders:
            self.create_content_entry(order.ticker)
            self.add_order_to_content(order.ticker, order)

        # --> Initialise history lsts
        self.orders_history = []

        self.net_worth_history = []
        self.funds_history = []
        self.net_profit_percentage_history = []
        self.day_profit_percentage_history = []

        # ---- Current param setup
        self.current_funds = initial_funds
        self.current_date = None

        # ---- Simple investment initialisation
        self.simple_investment_assets = None
        self.simple_investment_net_worth = []

    def create_content_entry(self, ticker, current_value=None):
        self.content[ticker] = {}
        self.content[ticker]["Current_price"] = current_value
        self.content[ticker]["Open_order_count"] = 0
        self.content[ticker]["Open_orders"] = []
        self.content[ticker]["Close_order_count"] = 0
        self.content[ticker]["Close_orders"] = []
        self.content[ticker]["Net_worth"] = []

    def add_order_to_content(self, ticker, order):
        self.content[ticker]["Open_orders"].append(order)
        self.content[ticker]["Open_order_count"] += 1

    def update_account(self, current_date, current_values):
        """
        Used to update daily values of the account, should always be ran first if new day!
        New tickers can be included here.

        :param current_date: Current traded date as string
        :param current_values: Dictionary of current values with tickers as key
        """
        self.current_date = current_date

        for ticker in self.content.keys():
            assert ticker in current_values.keys()

        # --> Update current prices and add new tickers
        for ticker in current_values.keys():
            if ticker not in self.content.keys():
                self.create_content_entry(ticker, current_values[ticker])
            else:
                self.content[ticker]["Current_price"] = current_values[ticker]

        # --> Update orders
        for ticker in current_values.keys():
            if len(self.content[ticker]["Open_orders"]) != 0:
                for order in self.content[ticker]["Open_orders"]:
                    order.update_order(current_values[ticker])

    def convert_funds_to_assets(self, ticker, investment_per_trade):
        """
        Used to perform a buy operation for a specific ticker at a given date

        :param ticker: Ticker traded
        :param investment_per_trade: Amount of investment to be performed
        """

        self.add_order_to_content(ticker, ORDER_gen(ticker,
                                                    self.current_date,
                                                    investment_per_trade/self.content[ticker]["Current_price"],
                                                    self.content[ticker]["Current_price"]))

        # --> Update funds
        self.current_funds = self.current_funds - investment_per_trade

    def convert_assets_to_funds(self, ticker, assets_sold_per_trade):
        """
        Used to perform a sell operation for a specific ticker at a given date

        :param ticker: Ticker traded
        :param assets_sold_per_trade: Amount of assets to be sold
        """
        # TODO: Develop order sell choice

        sell_worth = 0
        while sell_worth < assets_sold_per_trade:
            # --> Select which order to close
            if len(self.content[ticker]["Open_orders"]) > 1:
                diff = []

                # --> Calc orders value-difference
                for order in self.content[ticker]["Open_orders"]:
                    diff.append(abs(assets_sold_per_trade - order.current_worth))

                # --> Rearrange orders according to value difference (min to max)
                for i in range(1, len(diff)):
                    if diff[i] < diff[i - 1]:
                        diff[i], diff[i - 1] = diff[i - 1], diff[i]
                        self.content[ticker]["Open_orders"][i], self.content[ticker]["Open_orders"][i - 1] = \
                            self.content[ticker]["Open_orders"][i - 1], self.content[ticker]["Open_orders"][i]

            # --> Close order
            order = self.content[ticker]["Open_orders"][0]
            order.close_order()

            # --> Record close worth
            sell_worth += order.close_worth

            # --> Move closed order to order history
            self.orders_history.append(self.content[ticker]["Open_orders"].pop(order))
            self.content[ticker]["Open_order_count"] -= 1

            if self.content[ticker]["Open_order_count"] == 0:
                break

        # --> Update funds
        self.current_funds = self.current_funds + sell_worth

    # ----------------------------------- Net functions
    def calc_net_worth(self):
        """
        Used to compute current net worth

        :return: Net worth
        """
        net_worth = self.net_worth_history[-1]
        for order in self.open_orders:
            order.update_order(self.current_value)
            net_worth += order.current_order_worth

        return net_worth

    def record_net_worth(self):
        """
        Used to record current net worth to net_worth_history
        """
        self.net_worth_history.append(self.calc_net_worth())

    def calc_day_profit_percentage(self):
        """
        Used to compute current day profit percentage

        :return: Day profit percentage
        """
        return (self.calc_net_worth()-self.net_worth_history[-1])/self.net_worth_history[-1]

    def record_day_profit_percentage(self):
        """
        Used to record current day profit percentage
        """
        self.day_profit_percentage_history.append(self.calc_day_profit_percentage())

    # ----------------------------------- Ticker specific functions
    def calc_ticker_net_worth(self, ticker):
        """
        Used to compute net worth of a specific ticker

        :param ticker: Ticker to be evaluated
        :return: Ticker specific current worth
        """
        net_worth = 0
        for order in self.open_orders:
            if order.ticker == ticker:
                net_worth += order.current_worth

        return net_worth

    def calc_ticker_current_profit(self, ticker):
        """
        Used to compute profit of a specific ticker

        :param ticker: Ticker to be evaluated
        :return: Ticker specific current profit
        """
        profit = 0
        for order in self.open_orders:
            if order.ticker == ticker:
                profit += order.current_return

        return profit

    # ----------------------------------- Simple investment functions
    def start_simple_investment(self, tickers=[], initial_investments=[1000]):
        self.simple_investment = ORDER_gen(ticker, self.current_date, initial_investment/self.current_value, self.current_value)

    def calc_simple_investment_value(self):
        self.simple_investment_net_worth.append(self.simple_investment_assets*self.current_value)

    # ----------------------------------- Print/plot functions
    def print_account_status(self):
        print("Money =", self.current_funds, "$")
        print("Number of open orders =", len(self.open_orders))
        print("Total asset value=", self.calc_net_worth(), "$")

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
