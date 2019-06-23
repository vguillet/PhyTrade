"""
This Trade bot is optimised for the RUN_multi_trade_sim

Input that still require manual input:
    - Simple investment settings
    - Investment settings
"""
from PhyTrade.Settings.Tradebot_settings import Tradebot_settings
from PhyTrade.Trade_simulations.Tools.ACCOUNT_gen import ACCOUNT


class Tradebot_v5:
    def __init__(self,
                 tickers,
                 initial_funds=1000,
                 initial_account_content={},
                 initial_account_simple_investment_content={},
                 account_prev_stop_loss=0.85, account_max_stop_loss=0.75,
                 ticker_prev_stop_loss=0.85,
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

        :param initial_funds: Initial funds to be used
        :param initial_account_content: Initial content of account
        :param initial_account_simple_investment_content: Initial simple investment content of account
        :param account_prev_stop_loss: Stop loss as % of previous day value for accounts
        :param account_max_stop_loss: Stop loss as % of max worth achieved for accounts
        :param ticker_prev_stop_loss: Stop loss as % of previous day value for tickers

        :param print_trade_process: Print trade process to console and plot profit per slice graphs
        """

        # ============================ TRADE_BOT ATTRIBUTES ============================
        # ~~~~~~~~~~~~~~~~ Settings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ---- Fetch tradebot settings
        settings = Tradebot_settings()
        settings.gen_tradebot_settings()

        # --> Simple investment settings
        self.s_initial_investment = settings.s_initial_investment

        # --> Investment settings
        self.fixed_investment = settings.fixed_investment
        self.investment_percentage = settings.investment_percentage

        self.asset_liquidation_percentage = settings.asset_liquidation_percentage

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.print_trade_process = print_trade_process
        self.initial_funds = initial_funds

        # ---- Tradebot finance
        self.account = ACCOUNT(tickers,
                               initial_funds=initial_funds,
                               initial_content=initial_account_content,
                               initial_simple_investment_content=initial_account_simple_investment_content)

        # --> Setup stop_losses
        self.account_prev_stop_loss = account_prev_stop_loss
        self.account_max_stop_loss = account_max_stop_loss

        self.ticker_prev_stop_loss = ticker_prev_stop_loss

        # --> Setup counters
        self.buy_count = 0
        self.sell_count = 0
        self.account_stop_loss_count = 0
        self.ticker_stop_loss_count = 0

    def calc_investment_value(self,
                              investment_settings,
                              max_investment_per_trade, signal_strength):
        """
        Used to generate trading values to be used for run_trade

        :param investment_settings: Investing protocol
        :param max_investment_per_trade: Maximum investment per trade allowed
        :param signal_strength: Signal strength to be used for scaling trading values

        :return investment_per_trade
        """

        # ~~~~~~~~~~~~~~~~~~ Define the investment per trade
        # --> Fixed investment value per trade
        if investment_settings == 0:
            if self.account.current_funds >= self.fixed_investment:
                investment_per_trade = self.fixed_investment
            else:
                investment_per_trade = self.account.current_funds
        # --> Fixed investment percentage per trade
        elif investment_settings == 1:
            investment_per_trade = self.account.current_funds * self.investment_percentage

        # --> Fixed investment value per trade pegged to signal strength
        elif investment_settings == 2:
            investment_per_trade = -((signal_strength - 1) * self.fixed_investment)

        # --> Fixed investment percentage per trade pegged to signal strength
        elif investment_settings == 3:
            investment_per_trade = -((signal_strength - 1) * self.account.current_funds * self.investment_percentage)

        else:
            investment_per_trade = 0
            print("Invalid investment per trade settings")

        # ----> Limit max investment per trade
        if investment_per_trade > max_investment_per_trade:
            investment_per_trade = max_investment_per_trade

        return investment_per_trade

    def calc_asset_sold_value(self, ticker, cash_in_settings=0, signal_strength=1):
        # ~~~~~~~~~~~~~~~~~~ Define the assets sold per trade
        # --> Total asset liquidation
        if cash_in_settings == 0:
            assets_sold_per_trade = self.account.content[ticker]["Net_worth"][-1]

        # --> Fixed asset liquidation percentage
        elif cash_in_settings == 1:
            assets_sold_per_trade = self.account.content[ticker]["Net_worth"][-1] * self.asset_liquidation_percentage

        # --> Asset liquidation percentage per trade pegged to signal strength
        elif cash_in_settings == 2:
            assets_sold_per_trade = (signal_strength + 1) * self.account.content[ticker]["Net_worth"][-1] * self.asset_liquidation_percentage

        else:
            assets_sold_per_trade = 0
            print("Invalid asset sold per trade settings")

        return assets_sold_per_trade

    def account_stop_loss(self):
        # --> Close all content orders
        for ticker in self.account.content.keys():
            self.account.close_all_ticker_order(ticker)

        # --> Update counter
        self.account_stop_loss_count += 1

        if self.print_trade_process:
            print("==========================================================")
            print("Account stop-loss triggered\n")
            self.account.print_account_status()
            print("==========================================================")

    def ticker_stop_loss(self, ticker):
        # --> Close all ticker orders
        self.account.close_all_ticker_order(ticker)

        # --> Update counter
        self.ticker_stop_loss_count += 1

        if self.print_trade_process:
            print("==========================================================")
            print("Ticker stop-loss triggered\n")
            print("")
            self.account.print_account_status()
            print("==========================================================")

    def perform_trade(self, ticker, trade_action,
                      investment_settings=1, max_investment_per_trade=50000, cash_in_settings=0, signal_strength=1):
        """
        Used to perform trade action

        :param ticker:  Traded ticker
        :param trade_action: Trade action to be performed
        :param investment_settings:
        :param max_investment_per_trade:
        :param cash_in_settings:
        :param signal_strength:
        """

        # ~~~~~~~~~~~~~~~~~~ Define trade protocol
        if self.print_trade_process:
            print("_______________________________")
            print("Ticker:", ticker)
        # --> For account
        if len(self.account.net_worth_history) != 0 \
                and self.account.net_worth_history[-1] < max(self.account.net_worth_history) * self.account_max_stop_loss\
                and self.account.current_order_count != 0:
            self.account_stop_loss()
            return

        if len(self.account.net_worth_history) > 1:
            if self.account.net_worth_history[-1] < self.account.net_worth_history[-2] * self.account_prev_stop_loss and self.account.current_order_count != 0:
                self.account_stop_loss()
                return

        # --> For ticker
        if len(self.account.net_worth_history) > 1:
            if self.account.content[ticker]["Net_worth"][-1] < self.account.content[ticker]["Net_worth"][-2] * self.ticker_prev_stop_loss \
                    and self.account.content[ticker]["Open_order_count"] != 0:
                self.ticker_stop_loss(ticker)
                return

        # ----- Define hold action
        if trade_action == 0:
            if self.print_trade_process:
                print("-> Hold\n")
            return

        # ----- Define buy action
        elif trade_action == -1:
            # --> Calculate investment per trade
            investment_per_trade = self.calc_investment_value(investment_settings=investment_settings,
                                                              max_investment_per_trade=max_investment_per_trade,
                                                              signal_strength=signal_strength)

            # --> Round according to current stock price
            asset_count = round(investment_per_trade/self.account.content[ticker]["Current_price"], 0)

            if not self.account.current_funds < self.account.content[ticker]["Current_price"]:
                self.account.convert_funds_to_assets(ticker, asset_count)
                self.buy_count += 1

                if self.print_trade_process:
                    print("Trade action: Buy")
                    print("Number of share brought:", asset_count)
                    print("Investment =", self.account.content[ticker]["Current_price"]*asset_count, "$\n")
                    self.account.print_account_status()
                return

            else:
                if self.print_trade_process:
                    print("Trade action 'Buy' canceled because insufficient funds\n")
                return

        # ----- Define sell action
        elif trade_action == 1:
            assets_sold_per_trade = self.calc_asset_sold_value(ticker,
                                                               cash_in_settings=cash_in_settings,
                                                               signal_strength=signal_strength)
            if self.account.content[ticker]["Open_order_count"] != 0:
                self.account.convert_assets_to_funds(ticker, assets_sold_per_trade)
                self.sell_count += 1

                if self.print_trade_process:
                    print("Trade action: Sell")
                    print("Asset worth sold =", assets_sold_per_trade, "$\n")
                    self.account.print_account_status()
                return

            else:
                if self.print_trade_process:
                    print("Trade action 'Sell' canceled because nothing to sell\n")
                return

        else:
            print(" --------------------------------------------------------> !!!!!!!!!!!!!!! ORDER NOT PROCESSED !!!!!!!!!!!!!!!")

    def print_tradebot_status(self):
        """
        Used to print tradebot status
        """
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Buy count =", self.buy_count)
        print("Sell count =", self.sell_count)
        print("Account stop_loss_count =", self.account_stop_loss_count)
        print("Ticker stop_loss_count =", self.ticker_stop_loss_count)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Starting funds:", self.initial_funds)
        print("\n~~~~~~~~~~~~~~")
        self.account.print_account_status()
