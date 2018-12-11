"""
This script contains the Volume class for all calculations relating to Volume

Victor Guillet
29/11/2018
"""


class VOLUME:
    def __init__(self, big_data, amplification_factor=1):
        from PhyTrade.Technical_Analysis.Tools.MATH_tools import MATH

        self.volume = big_data.volume
        self.amp_coef = []

        # Normalising volume signal values between 0 and 1
        self.amp_coef = MATH().normalise_zero_one(self.volume)

        # Amplifying volume signal
        self.amp_coef = MATH().amplify(self.amp_coef, amplification_factor)
