"""
This script contains the Volume class for all calculations relating to Volume

Victor Guillet
29/11/2018
"""


class VOLUME:
    def __init__(self, big_data, amplification_factor=1):
        """
        Calculate and generates amp_coef list based on volume to be used as an amplification signal

        :param big_data: BIGDATA class instance
        :param amplification_factor: Amplification factor of the signal
        """
        from PhyTrade.Tools.MATH_tools import MATH

        self.volume = big_data.volume
        self.amp_coef = []

        # Normalising volume signal values between 0 and 1
        self.amp_coef = MATH().normalise_zero_one(self.volume)

        # Amplifying volume signal
        self.amp_coef = MATH().amplify(self.amp_coef, amplification_factor)
