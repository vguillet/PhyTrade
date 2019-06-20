import time


class Progress_bar:
    def __init__(self, max_step, bar_size=30, label=None):

        # --> Initiate Progress bar
        self.bar_size = bar_size
        self.max_step = max_step
        self.step = max_step/self.bar_size

        self.current = 0
        if label is not None:
            self.label = label+" | "
        else:
            self.label = ""

        # --> Initiate time tracker
        self.start_time = time.time()
        self.run_time_lst = []

    def update_progress_bar(self, current):
        self.current = current+1
        self.run_time = -round(self.start_time - time.time(), 3)
        self.run_time_lst.append(self.run_time)

        print(self.build_bar())

        # --> Reset start time for next iteration
        self.start_time = time.time()

    def build_bar(self):
        # Construct bar
        bar = "["
        nb_of_steps = int(self.current / self.step)
        for _ in range(nb_of_steps):
            bar = bar + "="
        bar = bar + ">"
        for _ in range(self.bar_size-nb_of_steps):
            bar = bar + "."
        bar = bar + "]"

        # --> Compute ETA
        eta = round(sum(self.run_time_lst)/len(self.run_time_lst) * (self.max_step-self.current))

        return self.label+str(self.current) + "/" + str(self.max_step) + " - " + bar + " - Run time: " + str(self.run_time) + "s, - ETA: " + str(eta) + "s"
