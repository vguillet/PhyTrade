

class data_slice_info:

    def __init__(self, start_slice, slice_size):
        self.start_index = start_slice
        self.stop_index = start_slice + slice_size
        self.slice_size = slice_size

    def get_next_data_slice(self):
        self.start_index = self.start_index + self.slice_size * 2
