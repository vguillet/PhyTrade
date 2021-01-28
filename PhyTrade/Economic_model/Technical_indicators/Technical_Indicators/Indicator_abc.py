
##################################################################################################################
"""
Abstract class used for generating indicators
"""

# Built-in/Generic Imports
from abc import ABC, abstractmethod

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '11/28/2018'

##################################################################################################################


class Indicator_abc(ABC):
    @abstractmethod
    def get_output(self, big_data, include_triggers_in_bb_signal=False):
        pass
