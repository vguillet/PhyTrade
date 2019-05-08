import random


class EVOA_random_gen:

    def modify_param(self, offspring, parameter_type_to_modify):
        if parameter_type_to_modify == "timeframe":
            parameter = random.choice(list(offspring.parameter_dictionary["timeframe"]))

            offspring.parameter_dictionary["timeframe"][parameter] = \
                self.timeframe_gen(offspring.parameter_dictionary["timeframe"][parameter])

        elif parameter_type_to_modify == "rsi_standard_upper_thresholds":
            parameter = random.choice(list(offspring.parameter_dictionary["rsi_standard_upper_thresholds"]))

            offspring.parameter_dictionary["rsi_standard_upper_thresholds"][parameter] = \
                self.rsi_upper_threshold_gen(
                    offspring.parameter_dictionary["rsi_standard_upper_thresholds"][parameter])

        elif parameter_type_to_modify == "rsi_standard_lower_thresholds":
            parameter = random.choice(list(offspring.parameter_dictionary["rsi_standard_lower_thresholds"]))

            offspring.parameter_dictionary["rsi_standard_lower_thresholds"][parameter] = \
                self.rsi_lower_threshold_gen(
                    offspring.parameter_dictionary["rsi_standard_lower_thresholds"][parameter])

        elif parameter_type_to_modify == "smoothing_factors":
            parameter = random.choice(list(offspring.parameter_dictionary["smoothing_factors"]))

            offspring.parameter_dictionary["smoothing_factors"][parameter] = \
                self.smoothing_factor_gen(offspring.parameter_dictionary["smoothing_factors"][parameter])

        elif parameter_type_to_modify == "amplification_factor":
            parameter = random.choice(list(offspring.parameter_dictionary["amplification_factor"]))

            offspring.parameter_dictionary["amplification_factor"][parameter] = \
                self.amplification_factor_gen(
                    offspring.parameter_dictionary["amplification_factor"][parameter])

        elif parameter_type_to_modify == "weights":
            parameter = random.choice(list(offspring.parameter_dictionary["weights"]))

            offspring.parameter_dictionary["weights"][parameter] = \
                self.weight_gen(offspring.parameter_dictionary["weights"][parameter])

        elif parameter_type_to_modify == "major_spline_standard_upper_thresholds":
            parameter = random.choice(list(offspring.parameter_dictionary["major_spline_standard_upper_thresholds"]))

            offspring.parameter_dictionary["major_spline_standard_upper_thresholds"][parameter] = \
                self.major_spline_upper_threshold_gen(
                    offspring.parameter_dictionary["major_spline_standard_upper_thresholds"][parameter])

        elif parameter_type_to_modify == "major_spline_standard_lower_thresholds":
            parameter = random.choice(list(offspring.parameter_dictionary["major_spline_standard_lower_thresholds"]))

            offspring.parameter_dictionary["major_spline_standard_lower_thresholds"][parameter] = \
                self.major_spline_lower_threshold_gen(
                    offspring.parameter_dictionary["major_spline_standard_lower_thresholds"][parameter])

        return offspring

    # ===============================================================================
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
