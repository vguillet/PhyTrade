import random


class GA_random_gen:
    # ------- Timeframes
    @staticmethod
    def timeframe_random_gen():
        return random.randint(2, 20)

    @staticmethod
    def timeframe_gen(current_parameter):
        new_parameter = current_parameter + random.randint(-6, 6)
        if new_parameter < 3:
            new_parameter = 2
        return new_parameter

    # ------- Smoothing factors
    @staticmethod
    def smoothing_factor_random_gen():
        return random.uniform(0.0, 2.0)

    @staticmethod
    def smoothing_factor_gen(current_parameter):
        new_parameter = current_parameter + random.uniform(-1.0, 1.0)
        if new_parameter < 0:
            new_parameter = 0
        return new_parameter

    # ------- Amplification factors
    @staticmethod
    def amplification_factor_random_gen():
        return random.uniform(0.0, 3.0)

    @staticmethod
    def amplification_factor_gen(current_parameter):
        new_parameter = current_parameter + random.uniform(-1.5, 1.5)
        if new_parameter < 0:
            new_parameter = 0
        return new_parameter

    # ------- Weights
    @staticmethod
    def weight_random_gen():
        return random.uniform(0.0, 10.0)

    @staticmethod
    def weight_gen(current_parameter):
        new_parameter = current_parameter + random.uniform(-4.0, 4.0)
        if new_parameter < 0:
            new_parameter = 0
        return new_parameter

    # ------- RSI standard Upper/Lower thresholds
    @staticmethod
    def rsi_upper_threshold_random_gen():
        return random.randint(51, 90)

    @staticmethod
    def rsi_lower_threshold_random_gen():
        return random.randint(10, 49)

    @staticmethod
    def rsi_upper_threshold_gen(current_parameter):
        new_parameter = current_parameter + random.randint(-20, 20)
        if new_parameter < 51:
            new_parameter = 51

        if new_parameter > 90:
            new_parameter = 90

        return new_parameter

    @staticmethod
    def rsi_lower_threshold_gen(current_parameter):
        new_parameter = current_parameter + random.randint(-20, 20)
        if new_parameter > 49:
            new_parameter = 49

        if new_parameter < 10:
            new_parameter = 10
        return new_parameter

    # ------- Major spline standard upper/lower thresholds
    @staticmethod
    def major_spline_upper_threshold_random_gen():
        return random.uniform(0.3, 0.6)

    @staticmethod
    def major_spline_lower_threshold_random_gen():
        return random.uniform(-0.3, -0.6)

    @staticmethod
    def major_spline_upper_threshold_gen(current_parameter):
        new_parameter = current_parameter + random.uniform(-0.2, 0.2)

        if new_parameter < 0.3:
            new_parameter = 0.3

        if new_parameter > 0.6:
            new_parameter = 0.6

        return new_parameter

    @staticmethod
    def major_spline_lower_threshold_gen(current_parameter):
        new_parameter = current_parameter + random.uniform(-0.2, 0.2)
        if new_parameter > -0.3:
            new_parameter = -0.3

        if new_parameter < -0.6:
            new_parameter = -0.6

        return new_parameter
