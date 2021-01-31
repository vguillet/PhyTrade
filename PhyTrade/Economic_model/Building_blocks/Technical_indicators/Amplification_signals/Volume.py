
##################################################################################################################
"""
This script contains the Volume class for all calculations relating to Volume
"""

# Libs
import numpy as np

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '29/11/2018'

##################################################################################################################


class Volume:
    def __init__(self, big_data, amplification_factor=1):
        """
        Calculate and generates amp_coef list based on volume to be used as an amplification signal

        :param big_data: BIGDATA class instance
        :param amplification_factor: Amplification factor of the signal
        """
        from PhyTrade.Tools.Math_tools import Math_tools

        self.volume = np.array(big_data.data_slice.subslice_data["Volume"])

        # Normalising volume signal values between 0 and 1
        self.amp_coef = Math_tools().normalise_zero_one(signal=self.volume)

        # Amplifying volume signal
        self.amp_coef = Math_tools().amplify(signal=self.amp_coef,
                                             amplification_factor=amplification_factor)
