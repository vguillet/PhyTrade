
##################################################################################################################
"""
Used to generate metalabels based on the peak-dip/simple/hybrid methods
"""

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class MetaLabels_gen:
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
            self.metalabels = self.peak_dip_metalabel_data(self.data_slice.sliced_data_selection)

        # --> Simple labels
        elif metalabel_setting == 1:
            self.metalabels = self.simple_metalabel_data(self.data_slice,
                                                         upper_barrier,
                                                         lower_barrier,
                                                         self.look_ahead)

        # --> Simple labels
        elif metalabel_setting == 2:
            self.metalabels = self.hybrid_metalabel_data(self.data_slice,
                                                         upper_barrier,
                                                         lower_barrier,
                                                         self.look_ahead)

    def peak_dip_metalabel_data(self, sliced_data):

        labels = [0]*len(sliced_data)

        # --> Initialise trend tracking
        if sliced_data[1] > sliced_data[0]:
            trend = "UP"
        else:
            trend = "DOWN"

        # --> Locate peaks and dips
        for i in range(len(sliced_data)-1):
            if sliced_data[i+1] >= sliced_data[i]:
                if trend == "UP":
                    labels[i] = 0
                else:
                    labels[i] = -1
                    trend = "UP"

            elif sliced_data[i+1] <= sliced_data[i]:
                if trend == "DOWN":
                    labels[i] = 0
                else:
                    labels[i] = 1
                    trend = "DOWN"

        return labels

    def simple_metalabel_data(self, data_slice, upper_barrier, lower_barrier, look_ahead):

        sliced_data = data_slice.sliced_data_selection
        data = data_slice.data_selection
        
        labels = []

        for i in range(len(sliced_data)):
            # --> Day tracker
            j = i + 1

            # --> Compute difference from current day
            percent_difference = (data[data_slice.start_index+j]-data[data_slice.start_index+i])/data[data_slice.start_index+i]*100

            # --> While barriers not hit, compute next day percentage difference
            while not percent_difference >= upper_barrier and not percent_difference <= lower_barrier and j - i != look_ahead:
                j += 1
                if j >= len(data):
                    break
                percent_difference = (data[data_slice.start_index+j]-data[data_slice.start_index+i])/data[data_slice.start_index+i]*100

            if percent_difference >= upper_barrier:
                labels.append(-1)
            elif percent_difference <= lower_barrier:
                labels.append(1)
            else:
                labels.append(0)

        return labels

    def hybrid_metalabel_data(self, data_slice, upper_barrier, lower_barrier, look_ahead):
        sliced_data = data_slice.sliced_data_selection
        data = data_slice.data_selection

        labels = self.peak_dip_metalabel_data(sliced_data)

        # --> Filter labels by simple metalabel
        for i in range(len(labels)):
            # --> Day tracker
            j = i + 1

            if labels[i] != 0:
                labels[i] = 0
                # --> Compute difference from current day
                percent_difference = (data[data_slice.start_index + j] - data[data_slice.start_index + i]) / data[
                    data_slice.start_index + i] * 100

                # --> While barriers not hit, compute next day percentage difference
                while not percent_difference >= upper_barrier and not percent_difference <= lower_barrier and j - i != look_ahead:
                    j += 1
                    if j > len(data):
                        labels[i] = 0
                        break

                    percent_difference = (data[data_slice.start_index + j] - data[data_slice.start_index + i]) / data[
                        data_slice.start_index + i] * 100

                if percent_difference >= upper_barrier:
                    labels[i] = -1
                elif percent_difference <= lower_barrier:
                    labels[i] = 1

        return labels
