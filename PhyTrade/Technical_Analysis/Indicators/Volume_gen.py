"""
This script contains the Volume class for all calculations relating to Volume

Victor Guillet
29/11/2018
"""


class Volume:
    def __init__(self, big_data, amplification_factor=1):
        self.volume = big_data.volume
        self.amp_coef = []

        for i in range(len(big_data.data_slice)):
            self.amp_coef.append(
                ((self.volume[i]-min(self.volume))/(max(self.volume)-min(self.volume)))*amplification_factor)
