
##################################################################################################################
"""
This script contains the BIGDATA class, necessary to collect and move around data in the model generation prototypes
"""

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '11/28/2018'

##################################################################################################################


class BIGDATA:
    def __init__(self, data_slice):
        """
        Contains all the information relating to a specific analysis,
        modules can be called, and their instance attribute should be saved in the big_data instance
        (to enable attribute access anywhere inm the model).
        To compute specific attributes, run the corresponding Technical_Indicators/modules.
        The list of all options can be found in the PhyTrade Library file

        :param data_slice: DATA_SLICE class instance
        """
        self.buffer = 0
        self.data_slice = data_slice

        # --> Apply buffer to data slice
        self.data_slice.start_index -= self.buffer
        self.data_slice.slice_size += self.buffer

        self.sell_trigger_values = []
        self.buy_trigger_values = []

        self.sell_trigger_dates = []
        self.buy_trigger_dates = []

        self.content = {"indicators": {},
                        "splines": {}}

