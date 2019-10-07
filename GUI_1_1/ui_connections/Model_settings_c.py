
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import datetime

# Libs

# Own modules
from GUI_1_1.Tools.Settings_to_json import record_settings

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

##################################################################################################################


def save_model_settings(ui, location="Current_settings", name=""):
    model_settings = {}

    # ___________________________ Print/plot parameters ______________________
    model_settings["print_trade_process"] = ui.print_trade_process.isChecked()

    # ___________________________ Model parameters ___________________________
    model_settings["evaluation_name"] = ui.evaluation_name.text()

    record_settings(model_settings, location, name="model_settings"+"_"+name)

