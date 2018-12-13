

class ACCOUNT:
    def __init__(self, initial_funds=1000, initial_assets=0):

        self.initial_funds = initial_funds

        self.current_funds = initial_funds
        self.current_assets = initial_assets
        
        self.funds_history = [initial_funds]
        self.assets_history = [initial_assets]
    
    def convert_funds_to_assets(self, current_value, investment_per_trade):

        self.current_funds = self.current_funds - investment_per_trade
        self.current_assets = self.current_assets + investment_per_trade / current_value

        self.funds_history.append(self.current_funds)
        self.assets_history.append(self.current_assets)

    def convert_assets_to_funds(self, current_value, investment_per_trade):
        self.current_funds = self.current_funds + investment_per_trade
        self.current_assets = self.current_assets - investment_per_trade / current_value

        self.funds_history.append(self.current_funds)
        self.assets_history.append(self.current_assets)

    def calc_net_worth(self, current_value):
        return self.current_funds+self.current_assets*current_value

    def calc_net_profit(self, current_value):
        return self.current_funds+self.current_assets*current_value-self.initial_funds

    def max_net_worth(self):
        self.net_worth_history = []
        for i in range(len(self.funds_history)):
            self.net_worth_history.append(self.funds_history[i])
        return max(self.)
    



