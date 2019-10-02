
##################################################################################################################
"""
Contains settings for generating metalabels
"""

# Built-in/Generic Imports
import json

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class Metalabeling_settings:
    # =============================== METALABELS SETTINGS =========================
    def gen_metalabels_settings(self):
        metalabeling_settings = json.load(open(r"C:\Users\Victor Guillet\Google Drive\Computer science\2-Programing\Repos\Python\Steffegium\Data\Settings\Current_settings\EVOA_optimiser_settings_.json"))

        # -- Metalabeling settings:
        self.metalabeling_settings = ["Peak", "Simple", "Hybrid"]
        self.metalabeling_setting = self.metalabeling_settings.index(metalabeling_settings["metalabeling_setting"])

        self.upper_barrier = metalabeling_settings["upper_barrier"]
        self.lower_barrier = metalabeling_settings["lower_barrier"]
        self.look_ahead = metalabeling_settings["look_ahead"]
