import time
from math import modf


class Progress_bar:
    def __init__(self, max_step, bar_size=30, label=None, overwrite_setting=True):

        # --> Initiate Progress bar
        self.overwrite_setting = overwrite_setting

        self.bar_size = bar_size
        self.max_step = max_step
        self.step = max_step/self.bar_size
        self.current = 0

        # --> Add label if provided
        if label is not None:
            self.label = label+" | "
        else:
            self.label = ""

        # --> Initiated loading circle if overwrite setting is true and select style
        if overwrite_setting is True:
            self.circle_pos_lst = ["-", "\\", "|", "/"]
            # self.circle_pos_lst = [".  ", ".. ", "..."]

            self.current_circle_pos = 0

        # --> Initiate time tracker
        self.initial_start_time = time.time()
        self.start_time = self.initial_start_time
        self.run_time_lst = []

    def update_progress_bar(self, current):
        self.current = current+1
        self.run_time = round(time.time() - self.start_time, 3)
        self.run_time_lst.append(self.run_time)

        if self.overwrite_setting:
            print("\r"+self.__progress_bar, end="")
        else:
            print(self.__progress_bar)

        # --> Reset start time for next iteration
        self.start_time = time.time()

    # ===============================================================================
    # -------------------------- Loading bar properties -----------------------------
    # ===============================================================================
    @property
    def __progress_bar(self):
        # --> Construct bar
        return self.__loading_circle + self.label + self.__process_count + self.__bar + self.__run_time + self.__eta + self.__process_completed_msg

    @property
    def __process_count(self):
        return self.__aligned_number(self.current, len(str(self.max_step))) + "/" + str(self.max_step)

    @property
    def __bar(self):
        bar = " - ["
        nb_of_steps = int(self.current / self.step)
        for _ in range(nb_of_steps):
            bar = bar + "="
        bar = bar + ">"
        for _ in range(self.bar_size-nb_of_steps):
            bar = bar + " "
        bar = bar + "]"
        return bar

    @property
    def __run_time(self):
        if self.current == self.max_step:
            total_run_time_str = self.__formatted_time(round(time.time() - self.initial_start_time, 3))
            if len(total_run_time_str) > 0:
                return " - Total run time: " + total_run_time_str
            else:
                return ""
        else:
            run_time_str = self.__formatted_time(self.run_time)
            if len(run_time_str) > 0:
                return " - Run time: " + run_time_str
            else:
                return ""

    @property
    def __eta(self):
        eta_str = self.__formatted_time(sum(self.run_time_lst)/len(self.run_time_lst) * (self.max_step-self.current))

        if len(eta_str) > 0:
            return " - ETA: " + eta_str
        else:
            return ""

    @property
    def __process_completed_msg(self):
        if self.current == self.max_step:
            return " - Process Completed"
        else:
            return ""

    @property
    def __loading_circle(self):
        if self.overwrite_setting is True:
            self.current_circle_pos += 1
            if self.current_circle_pos > len(self.circle_pos_lst)-1:
                self.current_circle_pos = 0
            return "[" + self.circle_pos_lst[self.current_circle_pos] + "] "
        else:
            return ""

    # --> String formatting functions
    def __formatted_time(self, formatted_time):

        formatted_time = [0, formatted_time]
        
        time_dict_keys = ["seconds", "minutes", "hours", "days", "years"]
        time_dict = {"seconds": {"max": 60,
                                 "current": 0},
                     "minutes": {"max": 60,
                                 "current": 0},
                     "hours": {"max": 24,
                               "current": 0},
                     "days": {"max": 365,
                              "current": 0},
                     "months": {"max": 12,
                                "current": 0},
                     "years": {"max": 10,
                               "current": 0},
                     "decades": {"max": 10,
                                 "current": 0},
                     "centuries": {"max": 999999999999,
                                   "current": 0}
                     }

        current_time_key = 0
        while formatted_time[1] / time_dict[time_dict_keys[current_time_key]]["max"] > 1:
            formatted_time = list(modf(formatted_time[1] / time_dict[time_dict_keys[current_time_key]]["max"]))
            if current_time_key == 0:
                time_dict[time_dict_keys[current_time_key]]["current"] = round(formatted_time[0] * time_dict[time_dict_keys[current_time_key]]["max"], 2)
            else:
                time_dict[time_dict_keys[current_time_key]]["current"] = round(formatted_time[0] * time_dict[time_dict_keys[current_time_key]]["max"])

            current_time_key += 1

        if current_time_key != 0:
            time_dict[time_dict_keys[current_time_key]]["current"] = round(formatted_time[1])
        else:
            time_dict[time_dict_keys[current_time_key]]["current"] = round(formatted_time[1] + formatted_time[0], 2)

        time_str = ""
        for key in time_dict_keys:
            if time_dict[key]["current"] != 0:
                if key == "seconds":
                    if time_dict[key]["current"] != 1:
                        time_str = self.__aligned_number(time_dict[key]["current"], 5, align_side="right") + " " + key + ", " + time_str
                    else:
                        time_str = self.__aligned_number(time_dict[key]["current"], 5, align_side="right") + " " + key[:-1] + " , " + time_str

                elif key in ["minutes", "hours"]:
                    if time_dict[key]["current"] != 1:
                        time_str = self.__aligned_number(time_dict[key]["current"], 2) + " " + key + ", " + time_str
                    else:
                        time_str = self.__aligned_number(time_dict[key]["current"], 2) + " " + key[:-1] + " , " + time_str
                else:
                    if time_dict[key]["current"] != 1:
                        time_str = str(time_dict[key]["current"]) + " " + key + ", " + time_str
                    else:
                        time_str = str(time_dict[key]["current"]) + " " + key[:-1] + " , " + time_str

        return time_str[:-2]
    
    @staticmethod
    def __aligned_number(current, req_len, align_side="left"):
        current = str(current)

        while len(current) < req_len:
            if align_side == "left":
                current = "0" + current
            else:
                current = current + "0"
        return current


if __name__ == "__main__":
    maxi_step = 100
    bar = Progress_bar(maxi_step, label="Demo bar", overwrite_setting=False)

    for i in range(maxi_step):
        time.sleep(1)
        bar.update_progress_bar(i)

