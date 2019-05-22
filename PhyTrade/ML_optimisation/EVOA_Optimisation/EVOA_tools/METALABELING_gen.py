"""
This script contains the MetaLabeling class, used for generating the metalabels for each day
to be used by the EVOA Optimisation
"""
from PhyTrade.Economic_model.Technical_Analysis.Data_Collection_preparation.Fetch_technical_data import fetch_technical_data


class MetaLabeling:
    def __init__(self, ticker, upper_barrier, lower_barrier, look_ahead, data_slice_start_ind, data_slice_stop_ind):

        data = fetch_technical_data(ticker)
        self.data = data[data_slice_start_ind:data_slice_stop_ind]

        self.upper_barrier = upper_barrier
        self.lower_barrier = lower_barrier

        self.look_ahead = look_ahead

        # --------------------- List close/open values
        # ... in data
        self.data_open_values = []
        self.data_close_values = []

        for index, row in self.data.iterrows():
            self.data_close_values.append(row['Close'])
            self.data_open_values.append(row['Open'])

        # --------------------- MetaLabel all dates
        # TODO fix metalabels to allow for searching dates outside of data slice
        def simple_metalabel_data(data_lst, upper_barrier, lower_barrier, look_ahead):

            labels = []

            for i in range(len(data_lst)-1):
                j = i + 1
                percent_difference = (data_lst[j]-data_lst[i])/data_lst[i] * 100

                while not percent_difference >= upper_barrier and not percent_difference <= lower_barrier and j - i != look_ahead:
                    j += 1
                    if j >= len(data_lst):
                        break
                    percent_difference = (data_lst[j] - data_lst[i]) / data_lst[i] * 100

                if percent_difference >= upper_barrier:
                    labels.append(1)
                elif percent_difference <= lower_barrier:
                    labels.append(-1)
                else:
                    labels.append(0)
            labels.append(0)
            return labels

        def peak_dip_metalabel_data(data_lst, look_ahead):

            labels = []

            for i in range(len(data_lst)-1):
                j = i + 1
                max_percent_difference = (data_lst[j]-data_lst[i])/data_lst[i] * 100

                while j - i != look_ahead:
                    j += 1
                    if j >= len(data_lst):
                        break

                    percent_difference = (data_lst[j] - data_lst[i]) / data_lst[i] * 100

                    if abs(percent_difference) > abs(max_percent_difference):
                        max_percent_difference = percent_difference

                labels.append(max_percent_difference)

            labels.append(0)

            # Initialise trend tracking
            if labels[1] > labels[0]:
                trend = "UP"
            elif labels[1] == labels[0]:
                trend = "NEUTRAL"
            else:
                trend = "DOWN"

            value = labels[0]

            # Locate peaks and dips
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

        self.close_values_metalabels = peak_dip_metalabel_data(self.data_close_values,
                                                               self.look_ahead)

        # print(len(self.open_values_metalabels))
        # print(self.open_values_metalabels)
        # print(len(self.close_values_metalabels))
        # print(self.close_values_metalabels)
