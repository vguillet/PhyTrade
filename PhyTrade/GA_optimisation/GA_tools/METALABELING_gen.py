import pandas as pd


class MetaLabeling:
    def __init__(self, upper_barrier, lower_barrier, look_ahead, data_slice_start_ind, data_slice_stop_ind):
        # TODO Streamline csv reading process
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Steffegium\Data\AAPL_Yahoo_data.csv".replace(
            '\\', '/')

        data = pd.read_csv(path)
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

        self.open_values_metalabels = simple_metalabel_data(self.data_open_values,
                                                            self.upper_barrier,
                                                            self.lower_barrier,
                                                            self.look_ahead)

        self.close_values_metalabels = simple_metalabel_data(self.data_close_values,
                                                             self.upper_barrier,
                                                             self.lower_barrier,
                                                             self.look_ahead)

        print(len(self.open_values_metalabels))
        print(self.open_values_metalabels)
        print(len(self.close_values_metalabels))
        print(self.close_values_metalabels)
