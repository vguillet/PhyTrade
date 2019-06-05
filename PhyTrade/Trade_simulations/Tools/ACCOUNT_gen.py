"""
Contains information about a Tradebot's account, along with it's transaction history etc...
"""
from PhyTrade.Trade_simulations.Tools.ORDER_gen import ORDER_gen


class ACCOUNT:
    def __init__(self, initial_funds=1000, initial_orders=[], simple_investment_orders=[]):
        """
        Stores the states of a trading account. Stores account history in:
            -> funds_history

            -> assets_history

            -> net_worth_history

        Contains the convert funds-to-assets and convert assets-to-funds methods to perform transactions
        The update_account must be run for each new day to allow for a correct updating of the orders, including when an account
        instance is initiated

        :param initial_funds: Initial funds in the account
        :param initial_orders: Initial orders in the account (as order class instances)
        """

        # ---- Account initialisation
        self.initial_funds = initial_funds
        self.initial_orders = initial_orders

        # ---- Records initialisation
        # --> Initialise history lsts
        self.orders_history = []

        self.net_worth_history = []
        self.funds_history = []
        self.asset_worth_history = []

        # ---- Current param setup
        self.current_funds = initial_funds
        self.current_asset_worth = 0
        self.current_order_count = 0
        self.current_date = None

        # --> Record initial orders in content
        self.content = {}
        self.simple_investment_orders = {}

        for order in self.initial_orders:
            if order.ticker not in self.content.keys():
                self.create_content_entry(order.ticker)
                self.create_simple_investment_entry(order.ticker)
            self.add_order_to_content(order.ticker, order)

        # ---- Simple investment initialisation
        for order in simple_investment_orders:
            if order.ticker not in self.simple_investment_orders.keys():
                self.create_simple_investment_entry(order.ticker)
            self.add_simple_investment_order(order.ticker, order)

    # =================================== Account management functions
    # ----------------------------------- Account management and update functions
    def update_account(self, current_date, current_prices):
        """
        Used to update daily values of the account, should always be ran first if new day!
        New tickers can be included here.

        :param current_date: Current traded date as string
        :param current_prices: Dictionary of current prices with tickers as key
        """
        self.current_date = current_date

        # --> Check all req. date is present (if orders are currently open)
        for ticker in self.content.keys():
            if self.content[ticker]["Open_order_count"] != 0:
                assert ticker in current_prices.keys()

        # --> Update current prices and add new tickers
        for ticker in current_prices.keys():
            if ticker not in self.content.keys():
                self.create_content_entry(ticker, current_prices[ticker])
                self.create_simple_investment_entry(ticker, current_prices[ticker])
            else:
                self.content[ticker]["Current_price"] = current_prices[ticker]
                self.simple_investment_orders[ticker]["Current_price"] = current_prices[ticker]

        for ticker in current_prices.keys():
            # --> Update orders
            for order in self.content[ticker]["Open_orders"]:
                order.update_order(current_date, current_prices[ticker])

            # --> Update net worth
            self.content[ticker]["Net_worth"].append(self.calc_ticker_net_worth(ticker))

            # --> Update simple investment
            if self.simple_investment_orders[ticker]["Order"] is not None:
                self.simple_investment_orders[ticker]["Order"].update_order(current_date, current_prices[ticker])

                # --> Update net worth
                self.simple_investment_orders[ticker]["Net_worth"].append(self.simple_investment_orders[ticker]["Order"].current_worth)

        # Record history of account
        self.record_net_worth()
        self.record_asset_worth()

    def update_ticker_entry(self, ticker, current_date, current_price):
        """
        Used to update specific ticker entry

        :param ticker: Ticker of order
        :param current_date: Current traded date as string
        :param current_price: Dictionary of current prices with tickers as key
        :return:
        """
        # --> Update current prices
        self.content[ticker]["Current_price"] = current_price[ticker]

        # --> Update net worth
        self.content[ticker]["Net_worth"].append(self.calc_ticker_net_worth(ticker))

        # --> Update orders
        for order in self.content[ticker]["Open_orders"]:
            order.update_order(current_date, current_price[ticker])

    # ----------------------------------- Trading actions
    def convert_funds_to_assets(self, ticker, asset_count):
        """
        Used to perform a buy operation for a specific ticker at a given date

        :param ticker: Ticker traded
        :param asset_count: Amount of investment to be performed
        """
        # --> Create order
        self.add_order_to_content(ticker, ORDER_gen(ticker,
                                                    self.current_date,
                                                    asset_count,
                                                    self.content[ticker]["Current_price"]))

        # --> Update funds and ticker net worth
        self.content[ticker]["Net_worth"][-1] = self.calc_ticker_net_worth(ticker)
        self.current_funds -= self.content[ticker]["Open_orders"][-1].open_worth

    def convert_assets_to_funds(self, ticker, assets_sold_per_trade):
        """
        Used to perform a sell operation for a specific ticker at a given date

        :param ticker: Ticker traded
        :param assets_sold_per_trade: Amount of assets to be sold
        """
        # TODO: Develop order sell choice
        sell_worth = 0
        while sell_worth < assets_sold_per_trade:
            # --> Select which order to close if multiple
            if self.content[ticker]["Open_order_count"] > 1:
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
            self.current_funds += order.close_worth

            # --> Move closed order to order history
            self.content[ticker]["Open_orders"].remove(order)
            self.content[ticker]["Closed_orders"].append(order)

            # --> Edit counters
            self.content[ticker]["Open_order_count"] -= 1
            self.content[ticker]["Closed_orders_count"] += 1

            # --> Update current parameters
            self.current_asset_worth -= order.close_worth
            self.current_order_count -= 1

            if self.content[ticker]["Open_order_count"] == 0:
                break

        # --> Update funds and ticker net worth
        self.current_funds = self.current_funds + sell_worth
        self.content[ticker]["Net_worth"][-1] = self.calc_ticker_net_worth(ticker)

    def close_all_ticker_order(self, ticker):
        """
        Used to close all orders for a specific ticker

        :param ticker: Traded ticker
        """
        for order in self.content[ticker]["Open_orders"]:
            # --> Close order
            order.close_order()

            # --> Record close worth
            self.current_funds += order.close_worth

            # --> Move closed order to order history
            self.content[ticker]["Open_orders"].remove(order)
            self.content[ticker]["Closed_orders"].append(order)

            # --> Edit counters
            self.content[ticker]["Open_order_count"] -= 1
            self.content[ticker]["Closed_orders_count"] += 1

            # --> Update current parameters
            self.current_asset_worth -= order.close_worth
            self.current_order_count -= 1

    # =================================== Account generation functions
    # ----------------------------------- Ticker specific functions
    def create_content_entry(self, ticker, current_value=None):
        """
        Used to add ticker entry to account

        :param ticker: Ticker traded
        :param current_value: Current price, can be left to none
        """
        self.content[ticker] = {}
        self.content[ticker]["Current_price"] = current_value
        self.content[ticker]["Open_order_count"] = 0
        self.content[ticker]["Open_orders"] = []
        self.content[ticker]["Closed_orders_count"] = 0
        self.content[ticker]["Closed_orders"] = []
        self.content[ticker]["Net_worth"] = []

    def add_order_to_content(self, ticker, order):
        """
        Used to add order to oontent

        :param ticker: Ticker of order
        :param order: Order class instance
        """
        # --> Add order to content
        self.content[ticker]["Open_orders"].append(order)

        # --> Edit counters
        self.content[ticker]["Open_order_count"] += 1

        # --> Update current parameters
        self.current_asset_worth += order.current_worth
        self.current_order_count += 1

    def calc_ticker_net_worth(self, ticker):
        """
        Used to compute net worth of a specific ticker

        :param ticker: Ticker to be evaluated
        :return: Ticker specific current worth
        """
        net_worth = 0
        for order in self.content[ticker]["Open_orders"]:
            net_worth += order.current_worth

        return net_worth

    def calc_ticker_current_profit(self, ticker):
        """
        Used to compute profit of a specific ticker

        :param ticker: Ticker to be evaluated
        :return: Ticker specific current profit
        """
        profit = 0
        for order in self.content[ticker]["Open_orders"]:
            profit += order.current_return

        return profit

    # ----------------------------------- Simple investment functions
    def create_simple_investment_entry(self, ticker, current_value=None):
        self.simple_investment_orders[ticker] = {}
        self.simple_investment_orders[ticker]["Current_price"] = current_value
        self.simple_investment_orders[ticker]["Order"] = None
        self.simple_investment_orders[ticker]["Net_worth"] = []

    def add_simple_investment_order(self, ticker, order):
        self.simple_investment_orders[ticker]["Open_orders"] = order

    def start_simple_investment(self, ticker, initial_investment=1000):
        # --> Create order
        self.add_simple_investment_order(ticker, ORDER_gen(ticker,
                                                           self.current_date,
                                                           initial_investment/self.simple_investment_orders[ticker]["Current_price"],
                                                           self.simple_investment_orders[ticker]["Current_price"]))
        # --> Update ticker net worth
        self.content[ticker]["Net_worth"].append(self.simple_investment_orders[ticker]["Order"].current_worth)

    # ----------------------------------- Net functions
    def calc_net_worth(self):
        """
        Used to compute current net worth

        :return: Net worth
        """
        net_worth = self.current_funds

        for ticker in self.content.keys():
            if self.content[ticker]["Open_order_count"] != 0:
                for order in self.content[ticker]["Open_orders"]:
                    net_worth += order.current_worth

        return net_worth

    def record_net_worth(self):
        """
        Used to record current net worth to net_worth_history
        """
        self.net_worth_history.append(self.calc_net_worth())

    def calc_asset_worth(self):
        """
        Used to compute current asset worth

        :return: Asset worth
        """
        asset_worth = 0

        for ticker in self.content.keys():
            if self.content[ticker]["Open_order_count"] != 0:
                for order in self.content[ticker]["Open_orders"]:
                    asset_worth += order.current_worth

        return asset_worth

    def record_asset_worth(self):
        """
        Used to record current asset worth to net_worth_history
        """
        self.asset_worth_history.append(self.calc_asset_worth())

    # ----------------------------------- Print/plot functions
    def print_account_status(self):
        print("-> ACCOUNT status:")
        print("Current funds =", self.current_funds, "$")
        print("Open orders =")
        for ticker in self.content.keys():
            print(ticker, ":", self.content[ticker]["Open_order_count"])

        print("Total net worth=", self.calc_net_worth(), "$")

        print("")

    def plot_net_worth(self, dates):
        import matplotlib.pyplot as plt

        plt.plot(dates, self.net_worth_history, label="Net worth history")
        # plt.plot(dates, self.simple_investment_net_worth, label="Simple investment net worth")

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.legend()
        plt.title("Net worth over time")
        plt.xlabel("Trade date")
        plt.ylabel("Net worth ($)")
        plt.show()
