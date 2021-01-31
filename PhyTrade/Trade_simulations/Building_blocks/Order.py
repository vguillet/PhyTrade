
################################################################################################################
"""
Used for generating orders and storing order information
"""

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class Order:
    def __init__(self, ticker, open_date, asset_count, open_price):
        """
        Used to generate orders

        :param open_date: Date of order creation
        :param asset_count: Number of assets brought in the order
        :param open_price: Price at order creation
        """

        # ---- Define open order parameters
        self.ticker = ticker
        self.open_date = open_date
        self.open_price = open_price

        self.asset_count = asset_count
        self.open_worth = open_price*asset_count

        # ---- Define current order parameters
        self.current_date = open_date
        self.current_price = open_price
        self.current_worth = self.open_worth
        self.return_percent = 0
        self.current_return = 0

        # ---- Define close order parameters
        self.closed = False
        self.close_date = None
        self.close_price = None

        self.close_worth = None
        self.close_return = None
        self.return_outcome = None

    def update_order(self, current_date, current_price):
        """
        Used to update order parameters

        :param current_date: Date of order update
        :param current_price: Price at order update
        """

        self.current_date = current_date
        self.current_price = current_price
        self.current_worth = current_price * self.asset_count
        self.return_percent = ((current_price - self.open_price) / self.open_price) * 100
        self.current_return = self.asset_count * (current_price - self.open_price)

    def close_order(self):
        """
        Use to close order and update order parameters

        return_outcome is used to record whether order was profitable or not
        """

        self.closed = True
        self.close_date = self.current_date
        self.close_price = self.current_price

        self.close_worth = self.current_worth
        self.close_return = self.current_return

        if self.close_worth >= self.open_worth:
            self.return_outcome = 1
        else:
            self.return_outcome = 0

    def __str__(self):
        return self.ticker + " order - Asset count: " + str(self.asset_count) + ", Current worth: " + str(self.current_worth) + " (" + self.current_date + ")"