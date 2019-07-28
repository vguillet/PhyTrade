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

        # --> Initiated loading circle if overwrite setting is true
        if overwrite_setting is True:
            self.circle_pos_lst = ["-", "\\", "|", "/"]
            self.current_circle_pos = 0

        # --> Initiate time tracker
        self.start_time = time.time()
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

        if len(self.__eta) != 0:
            return self.__loading_circle + self.label \
                   + self.__aligned_number(self.current, len(str(self.max_step))) + "/" + str(self.max_step) \
                   + " - " + self.__bar \
                   + " - Run time: " + self.__aligned_number(self.run_time, 5, align_side="right") + "s, - ETA: " + self.__eta
        else:
            return self.label + self.__aligned_number(self.current, len(str(self.max_step))) + "/" + str(self.max_step) + " - " + self.__bar + " - Process Completed"

    @property
    def __bar(self):
        bar = "["
        nb_of_steps = int(self.current / self.step)
        for _ in range(nb_of_steps):
            bar = bar + "="
        bar = bar + ">"
        for _ in range(self.bar_size-nb_of_steps):
            bar = bar + " "
        bar = bar + "]"
        return bar

    @property
    def __eta(self):
        # --> Compute ETA
        eta_keys = ["seconds", "minutes", "hours", "days", "years"]

        eta = {"seconds": {"max": 60,
                           "current": 0.},
               "minutes": {"max": 60,
                           "current": 0.},
               "hours":  {"max": 24,
                          "current": 0.},
               "days":  {"max": 365,
                         "current": 0},
               "months": {"max": 12,
                          "current": 0},
               "years":  {"max": 99999999999,
                          "current": 0.}}

        modf_eta = [0, sum(self.run_time_lst)/len(self.run_time_lst) * (self.max_step-self.current)]

        current_eta_key = 0
        while modf_eta[1]/eta[eta_keys[current_eta_key]]["max"] > 1:
            modf_eta = list(modf(modf_eta[1]/eta[eta_keys[current_eta_key]]["max"]))
            eta[eta_keys[current_eta_key]]["current"] = round(modf_eta[0] * eta[eta_keys[current_eta_key]]["max"], 3)
            current_eta_key += 1

        if current_eta_key != 0:
            eta[eta_keys[current_eta_key]]["current"] = round(modf_eta[1])
        else:
            # eta[eta_keys[current_eta_key]]["current"] = round(modf_eta[1], 3)
            eta[eta_keys[current_eta_key]]["current"] = round(modf_eta[1] + modf_eta[0], 3)

        eta_str = ""
        for key in eta_keys:
            if eta[key]["current"] != 0:
                eta_str = str(eta[key]["current"]) + " " + key + ", " + eta_str

        if len(eta_str) > 0:
            return eta_str[:-2]
        else:
            return ""

    @property
    def __loading_circle(self):
        if self.overwrite_setting is True:
            self.current_circle_pos += 1
            if self.current_circle_pos > len(self.circle_pos_lst)-1:
                self.current_circle_pos = 0
            return self.circle_pos_lst[self.current_circle_pos] + " "
        else:
            return ""

    # --> Function to ensure number strings align
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
    bar = Progress_bar(maxi_step, overwrite_setting=True)

    for i in range(maxi_step):
        time.sleep(0.205)
        bar.update_progress_bar(i)

