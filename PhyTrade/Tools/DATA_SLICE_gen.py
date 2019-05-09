"""
This script contains the data_slice class used by the EVOA Optimisation. The slice itself contains
information about the slice analysed, including the starting and stopping index, along with the metalabels generated
"""
from PhyTrade.ML_optimisation.EVOA_Optimisation.EVOA_tools.METALABELING_gen import MetaLabeling


class data_slice_info:
    def __init__(self, start_slice, slice_size, data_slice_shift_per_gen,
                 upper_barrier, lower_barrier, look_ahead):

        self.start_index = start_slice
        self.stop_index = start_slice + slice_size

        self.slice_size = slice_size
        self.data_slice_shift_per_gen = data_slice_shift_per_gen

        self.upper_barrier = upper_barrier
        self.lower_barrier = lower_barrier
        self.look_ahead = look_ahead

        self.metalabels = MetaLabeling(self.upper_barrier, self.lower_barrier, self.look_ahead,
                                       self.start_index, self.stop_index)

    def get_next_data_slice(self):
        # -- Determine new start/stop indexes
        self.start_index = self.start_index + self.slice_size
        self.stop_index = self.stop_index + self.slice_size

        if self.stop_index >= 0:
            self.stop_index = 0

        # -- Obtain new metalabels
        self.metalabels = MetaLabeling(self.upper_barrier, self.lower_barrier, self.look_ahead,
                                       self.start_index, self.stop_index)

    def get_shifted_data_slice(self):
        # -- Determine new start/stop indexes
        self.start_index = self.start_index + self.data_slice_shift_per_gen
        self.stop_index = self.stop_index + self.data_slice_shift_per_gen

        if self.stop_index >= 0:
            self.stop_index = 0

        # -- Obtain new metalabels
        self.metalabels = MetaLabeling(self.upper_barrier, self.lower_barrier, self.look_ahead,
                                       self.start_index, self.stop_index)
