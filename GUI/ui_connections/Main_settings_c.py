
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import datetime

# Libs

# Own modules
from GUI.Tools.Settings_to_json import record_settings

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

##################################################################################################################


def save_market_settings(ui, location="Current_settings", name=""):
    # ---- Market settings
    market_settings = {}

    market_settings["tickers"] = ui.tickers.toPlainText().replace(" ", "").split(",")

    market_settings["reference_label"] = str(ui.refference_label.currentText())
    market_settings["reference_term"] = str(ui.refference_term.currentText())
    market_settings["price_selection"] = str(ui.price_selection.currentText())
    market_settings["data_slice_size"] = ui.data_slice_size.value()

    # ---- Date settings
    market_settings["training_start_date"] = ui.training_start_date.date().toPyDate().strftime('%Y-%m-%d')
    market_settings["training_stop_date"] = ui.training_stop_date.date().toPyDate().strftime('%Y-%m-%d')

    market_settings["testing_start_date"] = ui.testing_start_date.date().toPyDate().strftime('%Y-%m-%d')
    market_settings["testing_stop_date"] = ui.testing_stop_date.date().toPyDate().strftime('%Y-%m-%d')

    # ---- Broker settings
    market_settings["min_transaction_cost"] = ui.min_transaction_cost.value()
    market_settings["transaction_cost_per_share"] = ui.transaction_cost_per_share.value()

    record_settings(market_settings, location, name="Market_settings"+"_"+name)


def save_tradebot_settings(ui, location="Current_settings", name=""):
    tradebot_settings = {}

    # --> Simple investment settings
    tradebot_settings["s_initial_investment"] = ui.s_initial_investment.value()

    # --> Investment settings
    tradebot_settings["initial_investment"] = ui.initial_investment.value()

    tradebot_settings["fixed_investment"] = ui.fixed_investment.value()
    tradebot_settings["investment_percentage"] = ui.investment_percentage.value()
    tradebot_settings["asset_liquidation_percentage"] = ui.asset_liquidation_percentage.value()

    record_settings(tradebot_settings, location, name="Tradebot_settings"+"_"+name)
