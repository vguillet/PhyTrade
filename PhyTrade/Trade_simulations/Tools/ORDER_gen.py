

class ORDER_gen:
    def __init__(self, open_date, asset_count, open_price):
        """
        Used to generate orders

        :param open_date: Date of order creation
        :param asset_count: Number of assets brought in the order
        :param open_price: Price at order creation
        """
        # ---- Define open order parameters
        self.open_date = open_date
        self.open_price = open_price

        self.asset_count = asset_count
        self.open_order_worth = open_price*asset_count

        # ---- Define current order parameters
        self.current_order_worth = self.open_order_worth
        self.return_pct = 0
        self.current_return = 0

        # ---- Define close order parameters
        self.closed = False
        self.close_date = None
        self.close_price = None

        self.close_order_worth = None
        self.close_return = None
        self.return_outcome = None

    def update_order(self, current_price):
        """
        Used to update order parameters

        :param current_price: Price at order update
        """
        self.current_order_worth = current_price * self.asset_count
        self.return_pct = ((current_price - self.open_price) / self.open_price) * 100
        self.current_return = self.asset_count * (current_price - self.open_price)

    def close_order(self, close_date, close_price):
        """
        Use to close order and update order parameters

        return_outcome is used to record whether order was profitable or not

        :param close_date: Date of order close
        :param close_price: Price at order close
        """
        self.closed = True
        self.close_date = close_date
        self.close_price = close_price

        self.close_order_worth = close_price * self.asset_count
        self.close_return = self.asset_count * (close_price - self.open_price)

        if self.close_order_worth >= self.open_order_worth:
            self.return_outcome = 1
        else:
            self.return_outcome = 0
