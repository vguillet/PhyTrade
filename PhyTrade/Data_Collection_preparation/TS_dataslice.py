################################################################################################################
"""
This script contains the data_slice class used by the EVOA Optimisation. The slice itself contains
information about the slice analysed, including the starting and stopping index, along with the metalabels generated
"""

# Libs
import numpy as np

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'


################################################################################################################


class TS_dataslice:
    def __init__(self, data,
                 subslice_size, subslice_shift_per_step,
                 start_date, end_date=None,
                 data_looper=False):
        """
        TS_dataslice instances contain all the time series data in a given date/time interval. Instances are slices of
        a timeseries dataset, and are used to access and analyse subslices of the selected sample
        analyse slices of a timeseries sequentially. This specific implementation was designed for daily datapoints
        analysis

        TS_dataslice properties:
            self.data: Time series data of dataslice

            self.start_index: Main slice start index
            self.start_date: Date corresponding to main slice start index

            self.end_index: Main slice end index
            self.end_date: Date corresponding to main slice end index (can be none, in which case end_date = -1)

            self.subslice_start_index: Current subslice start index
            self.subslice_start_date: Date corresponding to current subslice start index

            self.default_subslice_size: Default subslice size, specified at initialisation (fixed)
            self.subslice_size: Subslice size adjusted according to data available (vary according to amount of data available)

            self.subslice_shift_per_step: How much is the subslice shifted

        :param data:
        :param subslice_size:
        :param subslice_shift_per_step:
        :param start_date:
        :param end_date:
        :param data_looper:
        """

        # ---- Data slice data
        self.data = data

        # ---- Subslice properties
        self.subslice_start_index = None
        self.subslice_stop_index = None

        self.default_subslice_size = subslice_size      # Fixed
        self.subslice_size = subslice_size              # Variable according to data

        self.subslice_shift_per_step = subslice_shift_per_step

        self.__set_subslice_properties(start_date)

        # ---- Main slice properties
        self.start_index = self.subslice_start_index
        self.start_date = self.subslice_start_date

        # --> Set end_date
        self.end_date = end_date
        if self.end_date is not None:
            try:
                self.end_index = -len(self.data) + np.flatnonzero(self.data['Date'] == self.end_date)[0]
            except:
                print("!!!!! End Date selected not present in data !!!!!")
        else:
            self.end_index = -1
            self.end_date = self.data.iloc[self.end_index]['Date']

        # self.data = self.data[self.start_index:self.end_index]

        # ---- Data slice settings
        self.data_looper = data_looper      # Disable/enable data looping
        self.end_of_dataset = False

    @property
    def subslice_start_date(self):
        return self.data.iloc[self.subslice_start_index]['Date']

    @property
    def subslice_stop_date(self):
        # Stop date is the date of index before stop index as stop index is not included in subslice
        return self.data.iloc[self.subslice_stop_index - 1]['Date']

    @property
    def subslice_data(self):
        return self.data[self.subslice_start_index:self.subslice_stop_index]

    def __set_subslice_properties(self, start_date):
        # --> Find corresponding starting data index from start date or shift to next day if not available
        found = False
        while found is not True:
            if start_date in list(self.data["Date"]):
                found = True
            else:
                print("!!! Start Date selected not present in data !!!")
                if int(start_date[-1]) == 9:
                    start_date = start_date[:-2] + str(int(start_date[-2]) + 1) + str(0)

                else:
                    start_date = start_date[:-1] + str(int(start_date[-1]) + 1)

                if int(start_date[-2:]) > 31:
                    raise ValueError("!!! Could not find a suitable starting date !!!\n\n")
                print("--> New start date selected:", start_date, "\n\n")

        self.subslice_start_index = -len(self.data) + np.flatnonzero(self.data['Date'] == start_date)[0]

        # --> Adjust slice size according to data available if necessary
        if len(self.data[self.subslice_start_index:]) < self.subslice_size:
            self.subslice_size = -len(self.data[self.subslice_start_index:])
            print("Data slice/subslice size adjusted to:", self.subslice_size,
                  " (== len(available data from specified starting date))")

        # TODO: Fix case of slice size bigger than start-end date interval
        # if len(self.data[self.start_index:-len(self.data)+np.flatnonzero(self.data['Date'] == end_date)[0]]) < self.slice_size:
        #     self.slice_size = -self.start_index + -len(self.data)+np.flatnonzero(self.data['Date'] == end_date)[0]

        # --> Find corresponding stop data index
        self.subslice_stop_index = self.subslice_start_index + self.subslice_size

        return

    def get_next_subslice(self, prints=True):
        # --> Determine new start/stop indexes
        self.subslice_start_index += self.subslice_size
        self.subslice_stop_index += self.subslice_size

        # --> Check for end of data
        self.check_end_data(prints)

    def get_shifted_subslice(self, prints=True):
        # --> Determine new start/stop indexes
        self.subslice_start_index = self.subslice_start_index + self.subslice_shift_per_step
        self.subslice_stop_index = self.subslice_stop_index + self.subslice_shift_per_step

        # --> Check for end of data
        self.check_end_data(prints)

    def check_end_data(self, prints):
        if self.end_date is None:
            if self.subslice_stop_index >= -1:
                if self.subslice_start_index < -1:
                    self.subslice_stop_index = -1
                    self.subslice_size = abs(self.subslice_start_index) - 1
                    return
                else:
                    if self.data_looper is True:
                        # --> Loop back to beginning of dataset if end of dataset is reached
                        self.subslice_size = self.default_subslice_size
                        self.subslice_start_index = self.start_index
                        self.subslice_stop_index = self.start_index + self.default_subslice_size
                        return
                    else:
                        # --> Trigger End of dataset
                        self.end_of_dataset = True
                        if prints:
                            print("\nEnd of dataset reached\n")
                        return
            else:
                return
        else:
            if self.subslice_stop_index > self.end_index:
                if self.subslice_start_index < self.end_index:
                    self.subslice_stop_index = self.end_index
                    self.subslice_size = abs(self.subslice_start_index - self.subslice_stop_index)
                    return
                else:
                    if self.data_looper is True:
                        # --> Loop back to beginning of dataset if end of dataset is reached
                        self.subslice_size = self.default_subslice_size
                        self.subslice_start_index = self.start_index
                        self.subslice_stop_index = self.start_index + self.default_subslice_size
                        return
                    else:
                        # --> Trigger End of dataset
                        self.end_of_dataset = True
                        if prints:
                            print("\nEnd of dataset reached\n")
                        return
            else:
                return

