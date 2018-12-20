"""
This script contains the data_slice class used by the genetic algorithm parameter optimisation
"""


class data_slice_info:
    def __init__(self, start_slice, slice_size, data_slice_shift_per_gen):
        self.start_index = start_slice
        self.stop_index = start_slice + slice_size

        self.slice_size = slice_size
        self.data_slice_shift_per_gen = data_slice_shift_per_gen

    def get_next_data_slice(self):
        self.start_index = self.start_index + self.slice_size
        self.stop_index = self.stop_index + self.slice_size

        if self.stop_index >= 0:
            self.stop_index = 0

    def get_shifted_data_slice(self):
        self.start_index = self.start_index + self.data_slice_shift_per_gen
        self.stop_index = self.stop_index + self.data_slice_shift_per_gen

        if self.stop_index >= 0:
            self.stop_index = 0
