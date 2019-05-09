# TODO create EMA indicator class

class EMA:
    def __init__(self, big_data, timeperiod_1=50, timeperiod_2=200):
        self.timeperiod_1 = timeperiod_1
        self.timeperiod_2 = timeperiod_2

        # --------------------------SMA CALCULATION---------------------------
        self.sma_1 = []
        self.sma_2 = []

        for i in range(len(big_data.data_slice)):

            # ------------------Calculate close values falling in timeperiod_1 and 2
            timeperiod_1_close_values = []
            timeperiod_2_close_values = []

            for j in range(self.timeperiod_1):
                timeperiod_1_close_values.append(big_data.data_open_values[big_data.data_slice_start_ind + i - j])

            for j in range(self.timeperiod_2):
                timeperiod_2_close_values.append(big_data.data_open_values[big_data.data_slice_start_ind + i - j])

            # ------------------Sum close values for timeperiod_1 and 2

            self.sma_1.append(sum(timeperiod_1_close_values)/len(timeperiod_1_close_values))
            self.sma_2.append(sum(timeperiod_2_close_values)/len(timeperiod_2_close_values))

            # ------------------Calculate the multiplier for weighting the EMA

            multiplier_1 = 2 / (self.timeperiod_1 + 1)
            multiplier_2 = 2 / (self.timeperiod_2 + 1)

            ema = []

