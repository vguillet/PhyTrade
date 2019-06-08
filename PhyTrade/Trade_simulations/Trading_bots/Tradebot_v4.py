"""
This Trade bot is optimised for the GA parameter optimisation, RUN_model, and RUN_single_trade_sim

Input that still require manual input:
    - Simple investment settings
    - Investment settings
"""
from SETTINGS import SETTINGS
from PhyTrade.Trade_simulations.Tools.S_ACCOUNT_gen import ACCOUNT


class Tradebot_v4:
    def __init__(self, daily_values,
                 trade_signal, trade_spline=[],
                 investment_settings=1, cash_in_settings=0,
                 initial_funds=1000,
                 initial_assets=0,
                 prev_stop_loss=0.85, max_stop_loss=0.75,
                 max_investment_per_trade=50000,
                 prev_simple_investment_assets=None,
                 print_trade_process=False):
        """
        Used to simulate a trade run based on a provided analysis.

        The investment settings are as follow:
            0 - Fixed investment value per trade

            1 - Fixed investment percentage per trade

            2 - Fixed investment value per trade pegged to signal strength

            3 - Fixed investment percentage per trade pegged to signal strength

        The cash-in settings are as follow:
            0 - Total asset liquidation

            1 - Fixed asset liquidation percentage

            2 - Asset liquidation percentage per trade pegged to signal strength

        :param investment_settings: Investing protocol
        :param cash_in_settings: Cash-in protocol
        :param initial_funds: Initial funds to be used
        :param initial_assets: Initial assets to be used
        :param prev_stop_loss: Stop loss as % of previous day value
        :param max_stop_loss: Stop loss as % of max worth achieved
        :param max_investment_per_trade: Maximum investment per trade allowed
        :param prev_simple_investment_assets: Number of shares from previous simple investment, keep to None to start new simple investment
        :param print_trade_process: Print trade process to console and plot profit per slice graphs
        """

        # ============================ TRADE_BOT ATTRIBUTES ============================
        # ~~~~~~~~~~~~~~~~ Settings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ---- Fetch tradebot settings
        settings = SETTINGS()
        settings.gen_tradebot_settings()

        # --> Simple investment settings
        self.s_initial_investment = settings.s_initial_investment

        # --> Investment settings
        self.fixed_investment = settings.fixed_investment
        self.investment_percentage = settings.investment_percentage

        self.asset_liquidation_percentage = settings.asset_liquidation_percentage

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.print_trade_process = print_trade_process

        # -- Tradebot finance
        self.account = ACCOUNT(initial_funds=initial_funds, initial_assets=initial_assets)
        self.prev_stop_loss = prev_stop_loss
        self.max_stop_loss = max_stop_loss

        self.buy_count = 0
        self.sell_count = 0
        self.stop_loss_count = 0
        
        # -- Daily stock prices
        self.daily_values = daily_values
        
        # -- Trade actions and spline
        self.trade_actions = trade_signal
        self.trade_spline = trade_spline

        # ==============================================================================
        """




        """
        # ============================ TRADE PROTOCOL DEF ==============================
        # ~~~~~~~~~~~~~~~~~~ Initiate simple investment
        if prev_simple_investment_assets is None:
            self.account.start_simple_investment(self.daily_values[0],
                                                 initial_investment=self.s_initial_investment)
        else:
            self.account.simple_investment_assets = prev_simple_investment_assets

        for i in range(len(self.trade_actions)):
            if self.print_trade_process:
                print("----------------- Day ", i)
                print("-------------------> Action", self.trade_actions[i])
                print("-------------------> Signal", self.trade_spline[i])

            # ~~~~~~~~~~~~~~~~~~ Calculate simple investment value
            self.account.calc_simple_investment_value(self.daily_values[i])

            # ~~~~~~~~~~~~~~~~~~ Define the investment per trade
            # --> Fixed investment value per trade
            if investment_settings == 0:
                if self.account.current_funds >= self.fixed_investment:
                    investment_per_trade = self.fixed_investment
                else:
                    investment_per_trade = self.account.current_funds
            # --> Fixed investment percentage per trade
            elif investment_settings == 1:
                investment_per_trade = self.account.current_funds*self.investment_percentage

            # --> Fixed investment value per trade pegged to signal strength
            elif investment_settings == 2:
                investment_per_trade = -((self.trade_spline[i]-1)*self.fixed_investment)

            # --> Fixed investment percentage per trade pegged to signal strength
            elif investment_settings == 3:
                investment_per_trade = -((self.trade_spline[i]-1)*self.account.current_funds*self.investment_percentage)

            else:
                investment_per_trade = 0

            # ----> Limit max investment per trade
            if investment_per_trade > max_investment_per_trade:
                investment_per_trade = max_investment_per_trade

            # ~~~~~~~~~~~~~~~~~~ Define the assets sold per trade
            # --> Total asset liquidation
            if cash_in_settings == 0:
                assets_sold_per_trade = self.account.current_assets

            # --> Fixed asset liquidation percentage
            elif cash_in_settings == 1:
                assets_sold_per_trade = self.account.current_assets*self.asset_liquidation_percentage

            # --> Asset liquidation percentage per trade pegged to signal strength
            elif cash_in_settings == 2:
                assets_sold_per_trade = (self.trade_spline[i]+1)*self.account.current_assets*self.asset_liquidation_percentage

            else:
                assets_sold_per_trade = 1000000

            # ~~~~~~~~~~~~~~~~~~ Define the variable stop-loss value
            # # TODO: Figure out variable stop_loss concept
            # if i % 100 == 0 and not self.prev_stop_loss == 0.95:
            #     self.prev_stop_loss += 0.01

            """


            """
            # ~~~~~~~~~~~~~~~~~~ Define trade protocol
            # ----- Define stop-loss action
            # --> WRT max_net_worth and/or prev_net_worth
            if not len(self.account.net_worth_history) == 0 and \
                    self.account.calc_net_worth(self.daily_values[i]) < \
                    max(self.account.net_worth_history) * self.max_stop_loss and \
                    not self.account.current_assets == 0 \
                    or\
                    not len(self.account.net_worth_history) == 0 and \
                    self.account.calc_net_worth(self.daily_values[i]) < \
                    self.account.net_worth_history[-1] * self.prev_stop_loss and \
                    not self.account.current_assets == 0:

                self.account.convert_assets_to_funds(
                    self.daily_values[i],
                    self.account.current_assets)

                self.stop_loss_count += 1

                if self.print_trade_process:
                    print("==========================================================")
                    print("Stop-loss triggered")
                    self.account.print_account_status(self.daily_values[i])
                    print("==========================================================")

            # ----- Define hold action
            elif self.trade_actions[i] == 0:
                self.account.record_net_worth(self.daily_values[i])

                if self.print_trade_process:
                    print("->Hold")

            # ----- Define buy action
            elif self.trade_actions[i] == -1:
                if self.account.current_funds != 0:
                    self.account.convert_funds_to_assets(
                        self.daily_values[i], investment_per_trade)
                    self.buy_count += 1

                    if self.print_trade_process:
                        print("Trade action: Buy")
                        print("Investment =", investment_per_trade, "$")
                        self.account.print_account_status(self.daily_values[i])

                else:
                    self.account.record_net_worth(self.daily_values[i])
                    if self.print_trade_process:
                        print("Trade action 'Buy' canceled because insufficient funds")

            # ----- Define sell action
            elif self.trade_actions[i] == 1:
                if self.account.current_assets != 0:
                    self.account.convert_assets_to_funds(
                        self.daily_values[i], assets_sold_per_trade)
                    self.sell_count += 1

                    if self.print_trade_process:
                        print("Trade action: Sell")
                        print("Investment =", investment_per_trade, "$")
                        self.account.print_account_status(self.daily_values[i])

                else:
                    self.account.record_net_worth(self.daily_values[i])
                    if self.print_trade_process:
                        print("Trade action 'Sell' canceled because nothing to sell")

        # ==============================================================================
        """




        """
        # ============================ TRADE RESULTS/RECAP =============================
        if self.print_trade_process:
            print("")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Buy count =", self.buy_count)
            print("Sell count =", self.sell_count)
            print("Stop_loss_count =", self.stop_loss_count)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Starting funds:", self.account.initial_funds)
            print("Starting assets:", self.account.initial_assets)
            print("")
            print("Current funds:", self.account.current_funds)
            print("Current assets:", self.account.current_assets)
            print("Net worth:", self.account.calc_net_worth(self.daily_values[-1]), "$")
            print("")
            print("Profit=", self.account.calc_net_profit(self.daily_values[-1]))
            print("Percent profit=", self.account.calc_net_profit(self.daily_values[-1]) / 10)
            print("")
            print("Max worth:", max(self.account.net_worth_history))
            print("Min worth:", min(self.account.net_worth_history))
            print("====================================================")
