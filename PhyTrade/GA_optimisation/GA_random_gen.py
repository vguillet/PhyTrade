import random


class GA_random_gen:
    # ------- Timeframe
    @staticmethod
    def timeframe_random_gen():
        return random.randint(2, 252)

    @staticmethod
    def timeframe_gen(current_parameter):
        new_parameter = current_parameter + random.randint(-6, 6)
        if new_parameter < 3:
            new_parameter = 2
        return new_parameter
    # ------- Smoothing factor
    @staticmethod
    def smoothing_factor_random_gen():
        return random.uniform(0.0, 2.0)

    @staticmethod
    def smoothing_factor_gen(current_parameter):
        new_parameter = current_parameter + random.uniform(-1.0, 1.0)
        if new_parameter < 0:
            new_parameter = 0
        return new_parameter

    # ------- Amplification factor
    @staticmethod
    def amplification_factor_random_gen():
        return random.uniform(0.0, 3.0)

    @staticmethod
    def amplification_factor_gen(current_parameter):
        new_parameter = current_parameter + random.uniform(-1.5, 1.5)
        if new_parameter < 0:
            new_parameter = 0
        return new_parameter

    # ------- Weight
    @staticmethod
    def weight_random_gen():
        return random.uniform(0.0, 10.0)

    @staticmethod
    def weight_gen(current_parameter):
        new_parameter = current_parameter + random.uniform(-4.0, 4.0)
        if new_parameter < 0:
            new_parameter = 0
        return new_parameter
