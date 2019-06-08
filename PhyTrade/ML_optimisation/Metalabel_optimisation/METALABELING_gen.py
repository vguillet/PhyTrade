"""
This script contains the MetaLabeling class, used for generating the metalabels for each day
to be used by the EVOA Optimisation
"""


class MetaLabeling:
    def __init__(self, upper_barrier, lower_barrier, look_ahead,
                 data_slice,
                 metalabel_setting=0):

        self.data_slice = data_slice

        self.upper_barrier = upper_barrier
        self.lower_barrier = lower_barrier

        self.look_ahead = look_ahead

        # --------------------- Metalabel data
        # --> Peak-dip labels
        if metalabel_setting == 0:
            self.metalabels = self.peak_dip_metalabel_data(self.data_slice.data_slice_selection,
                                                           self.look_ahead)

        # --> Simple labels
        elif metalabel_setting == 1:
            self.metalabels = self.simple_metalabel_data(self.data_slice.data_selection,
                                                         self.data_slice.data_slice_selection,
                                                         upper_barrier,
                                                         lower_barrier,
                                                         self.look_ahead)

    def peak_dip_metalabel_data(self, data_slice, look_ahead):

        labels = []

        for i in range(len(data_slice)-1):
            j = i + 1
            max_percent_difference = (data_slice[j]-data_slice[i])/data_slice[i] * 100

            while j - i != look_ahead:
                j += 1
                if j >= len(data_slice):
                    break

                percent_difference = (data_slice[j] - data_slice[i])/data_slice[i] * 100

                if abs(percent_difference) > abs(max_percent_difference):
                    max_percent_difference = percent_difference

            labels.append(max_percent_difference)

        labels.append(0)

        # --> Initialise trend tracking
        if labels[1] > labels[0]:
            trend = "UP"
        elif labels[1] == labels[0]:
            trend = "NEUTRAL"
        else:
            trend = "DOWN"

        value = labels[0]

        # --> Locate peaks and dips
        for i in range(len(labels)-1):
            if trend == "UP":
                if labels[i+1] >= value:
                    labels[i] = 0

                    value = labels[i+1]
                else:
                    labels[i] = 1
                    trend = "DOWN"

                    value = labels[i + 1]

            elif trend == "NEUTRAL":
                labels[i] = 0
                value = labels[i + 1]

            elif trend == "DOWN":
                if labels[i+1] <= value:
                    labels[i] = 0
                    value = labels[i+1]
                else:
                    labels[i] = -1
                    trend = "UP"

        return labels

    # TODO fix metalabels to allow for searching dates outside of data slice
    def simple_metalabel_data(self, data, data_slice, upper_barrier, lower_barrier, look_ahead):

        labels = []

        for i in range(len(data_slice)-1):
            j = i + 1
            percent_difference = (data_slice[j]-data_slice[i])/data_slice[i] * 100

            while not percent_difference >= upper_barrier and not percent_difference <= lower_barrier and j - i != look_ahead:
                j += 1
                if j >= len(data_slice):
                    break
                percent_difference = (data_slice[j] - data_slice[i]) / data_slice[i] * 100

            if percent_difference >= upper_barrier:
                labels.append(1)
            elif percent_difference <= lower_barrier:
                labels.append(-1)
            else:
                labels.append(0)

        labels.append(0)

        return labels


        # self.open_values_metalabels = simple_metalabel_data(self.data_open_values,
        #                                                     self.upper_barrier,
        #                                                     self.lower_barrier,
        #                                                     self.look_ahead)

        # self.close_values_metalabels = simple_metalabel_data(self.data_close_values,
        #                                                      self.upper_barrier,
        #                                                      self.lower_barrier,
        #                                                      self.look_ahead)

        # self.open_values_metalabels = peak_dip_metalabel_data(self.data_open_values,
        #                                                       self.look_ahead)

        # print(len(self.open_values_metalabels))
        # print(self.open_values_metalabels)
        # print(len(self.close_values_metalabels))
        # print(self.close_values_metalabels)
