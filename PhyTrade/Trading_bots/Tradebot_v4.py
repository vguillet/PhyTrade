"""
This Trade bot is optimised for the GA parameter optimisation

"""

from PhyTrade.Trading_bots.ACCOUNT_tools import ACCOUNT
import matplotlib.pyplot as plt


class Tradebot_v4:
    def __init__(self, analysis,
                 investment_settings=3, cash_in_settings=0,
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

        :param analysis: Analysis to be used for performing trade decisions
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
        print_trade_process = print_trade_process

        # -- Tradebot finance
        self.account = ACCOUNT(initial_funds=initial_funds, initial_assets=initial_assets)
        self.prev_stop_loss = prev_stop_loss
        self.max_stop_loss = max_stop_loss

        stop_loss_count = 0

        # -- Market analysis protocol
        self.analysis = analysis

        # -- Generate trade actions from analysis
        self.trade_actions = [0] * len(self.analysis.big_data.data_slice_dates)

        if analysis.big_data.buy_sell_labels is None:
            for i in self.analysis.big_data.Major_spline.sell_dates:
                self.trade_actions[self.analysis.big_data.data_slice_dates.index(i)] = 1

            for i in self.analysis.big_data.Major_spline.buy_dates:
                self.trade_actions[self.analysis.big_data.data_slice_dates.index(i)] = -1

        # TODO: check for use of buy_sell_labels
        else:
            for i in range(len(analysis.big_data.buy_sell_labels)):
                if analysis.big_data.buy_sell_labels[i] == 1:
                    self.trade_actions[i] = 1

                elif analysis.big_data.buy_sell_labels[i] == -1:
                    self.trade_actions[i] = -1

        # ==============================================================================
        """




        """
        # ============================ TRADE PROTOCOL DEF ==============================
        # ~~~~~~~~~~~~~~~~~~ Initiate simple investment
        if prev_simple_investment_assets is None:
            self.account.start_simple_investment(self.analysis.big_data.data_slice_open_values[0], initial_investment=1000)
        else:
            self.account.simple_investment_assets = prev_simple_investment_assets

        for i in range(len(self.trade_actions)):
            if print_trade_process:
                print("----------------- Day ", i)

            # ~~~~~~~~~~~~~~~~~~ Calculate simple investment value
            self.account.calc_simple_investment_value(self.analysis.big_data.data_slice_open_values[i])

            # ~~~~~~~~~~~~~~~~~~ Define the investment per trade
            # --> Fixed investment value per trade
            if investment_settings == 0:
                if self.account.current_funds >= 100:
                    investment_per_trade = 100
                else:
                    investment_per_trade = self.account.current_funds
            # --> Fixed investment percentage per trade
            elif investment_settings == 1:
                investment_per_trade = self.account.current_funds * 0.3

            # --> Fixed investment value per trade pegged to signal strength
            elif investment_settings == 2:
                investment_per_trade = -((self.analysis.big_data.Major_spline.spline[i]-1)*100)

            # --> Fixed investment percentage per trade pegged to signal strength
            elif investment_settings == 3:
                investment_per_trade = -((self.analysis.big_data.Major_spline.spline[i]-1)*self.account.current_funds * 0.2)

            # ----> Limit max investment per trade
            if investment_per_trade > max_investment_per_trade:
                investment_per_trade = max_investment_per_trade

            # ~~~~~~~~~~~~~~~~~~ Define the assets sold per trade
            # --> Total asset liquidation
            if cash_in_settings == 0:
                assets_sold_per_trade = self.account.current_assets

            # --> Fixed asset liquidation percentage
            elif cash_in_settings == 1:
                assets_sold_per_trade = self.account.current_assets * 0.3

            # --> Asset liquidation percentage per trade pegged to signal strength
            elif cash_in_settings == 2:
                assets_sold_per_trade = (self.analysis.big_data.Major_spline.spline[i]+1) * self.account.current_assets * 0.3

            # ~~~~~~~~~~~~~~~~~~ Define the variable stop-loss value
            # TODO: Figure out variable stop_loss concept
            if i % 100 == 0 and not self.prev_stop_loss == 0.95:
                self.prev_stop_loss += 0.01

            """


            """
            # ~~~~~~~~~~~~~~~~~~ Define trade protocol
            # ----- Define stop-loss action
            # --> WRT max_net_worth and/or prev_net_worth
            if not len(self.account.net_worth_history) == 0 and \
                    self.account.calc_net_worth(self.analysis.big_data.data_slice_open_values[i]) < \
                    max(self.account.net_worth_history) * self.max_stop_loss and \
                    not self.account.current_assets == 0 \
                    or\
                    not len(self.account.net_worth_history) == 0 and \
                    self.account.calc_net_worth(self.analysis.big_data.data_slice_open_values[i]) < \
                    self.account.net_worth_history[-1] * self.prev_stop_loss and \
                    not self.account.current_assets == 0:

                self.account.convert_assets_to_funds(
                    self.analysis.big_data.data_slice_open_values[i],
                    self.account.current_assets)

                stop_loss_count += 1

                if print_trade_process:
                    print("==========================================================")
                    print("Stop-loss triggered")
                    self.account.print_account_status(self.analysis.big_data.data_slice_open_values[i])
                    print("==========================================================")

            # ----- Define hold action
            elif self.trade_actions[i] == 0:
                self.account.record_net_worth(self.analysis.big_data.data_slice_open_values[i])

                if print_trade_process:
                    print("->Hold")

            # ----- Define buy action
            elif self.trade_actions[i] == -1 and not self.account.current_funds == 0:
                self.account.convert_funds_to_assets(
                    self.analysis.big_data.data_slice_open_values[i], investment_per_trade)

                if print_trade_process:
                    print("Trade action: Buy")
                    print("Investment =", investment_per_trade, "$")
                    self.account.print_account_status(self.analysis.big_data.data_slice_open_values[i])

            # ----- Define sell action
            elif self.trade_actions[i] == 1 and not self.account.current_assets == 0:
                self.account.convert_assets_to_funds(
                    self.analysis.big_data.data_slice_open_values[i], assets_sold_per_trade)

                if print_trade_process:
                    print("Trade action: Sell")
                    print("Investment =", investment_per_trade, "$")
                    self.account.print_account_status(self.analysis.big_data.data_slice_open_values[i])

            else:
                self.account.record_net_worth(self.analysis.big_data.data_slice_open_values[i])

                if print_trade_process:
                    print("Trade action 'Sell' canceled because nothing to sell")

        # ==============================================================================
        """




        """
        # ============================ TRADE RESULTS/RECAP =============================
        if print_trade_process:
            print("")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Buy count =", len(self.analysis.big_data.Major_spline.buy_dates))
            print("Sell count =", len(self.analysis.big_data.Major_spline.sell_dates))
            print("Stop_loss_count =", stop_loss_count)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Starting funds:", self.account.initial_funds)
            print("Starting assets:", self.account.initial_assets)
            print("")
            print("Current funds:", self.account.current_funds)
            print("Current assets:", self.account.current_assets)
            print("Net worth:", self.account.calc_net_worth(self.analysis.big_data.data_slice_open_values[-1]), "$")
            print("")
            print("Profit=", self.account.calc_net_profit(self.analysis.big_data.data_slice_open_values[-1]))
            print("Percent profit=", self.account.calc_net_profit(self.analysis.big_data.data_slice_open_values[-1]) / 10)
            print("")
            print("Max worth:", max(self.account.net_worth_history))
            print("Min worth:", min(self.account.net_worth_history))
            print("====================================================")

            self.account.plot_net_worth(self.analysis.big_data.data_slice_dates)


