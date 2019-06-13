import time


class Progress_bar:
    def __init__(self, max_step):

        # --> Initiate Progress bar
        self.max = max_step
        self.step = max_step/30

        self.current = 0

        # --> Initiate time tracker
        self.start_time = time.time()

    def update_progress_bar(self, current):
        self.current = current+1
        self.run_time = round(self.start_time - time.time(), 3)

        print(self.build_bar())

        self.start_time = time.time()

    def build_bar(self):
        bar = "["

        nb_of_steps = int(self.current / self.step)
        for _ in range(nb_of_steps):
            bar = bar + "="

        bar = bar + ">"

        for _ in range(30-nb_of_steps):
            bar = bar + "."

        bar = bar + "]"

        return str(self.current) + "/" + str(self.max) + " - " + bar + " - Run time: " + str(-self.run_time) + "s"
