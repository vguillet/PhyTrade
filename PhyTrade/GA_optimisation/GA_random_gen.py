import random


class GA_random_gen:
    @staticmethod
    def timeframe_gen():
        return random.randint(2, 100)

    @staticmethod
    def smoothing_factor_gen():
        return random.uniform(0.0, 2.0)

    @staticmethod
    def amplification_factor_gen():
        return random.uniform(0.0, 3.0)

    @staticmethod
    def weight_gen():
        return random.uniform(0.0, 10.0)
