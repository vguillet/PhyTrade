
##################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from GUI_1_1.Tools.Settings_to_json import record_settings

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

##################################################################################################################


def get_simple_metalabels_settings(ui, location="Current_settings"):
    simple_metalabels_settings = {}

    # -- Metalabeling settings:
    simple_metalabels_settings["metalabeling_setting"] = str(ui.metalabeling_setting.currentText())

    simple_metalabels_settings["upper_barrier"] = ui.upper_barrier.value()
    simple_metalabels_settings["lower_barrier"] = ui.lower_barrier.value()
    simple_metalabels_settings["look_ahead"] = ui.look_ahead.value()

    record_settings(simple_metalabels_settings, location, name="simple_metalabels_settings")
