
##################################################################################################################
"""
Contains settings for generating metalabels
"""

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class Metalabeling_settings:
    # =============================== METALABELS SETTINGS =========================
    def gen_metalabels_settings(self):
        # -- Metalabeling settings:
        self.metalabeling_settings = ["Peak", "Simple", "Hybrid"]
        self.metalabeling_setting = 0

        self.upper_barrier = 20
        self.lower_barrier = -20
        self.look_ahead = 20
