import random
from PhyTrade.ML_optimisation.EVOA_Optimisation.EVOA_tools.EVOA_tools import EVOA_tools


class EVOA_random_gen:

    def modify_param(self, offspring, parameter_type_to_modify,
                     current_generation, nb_of_generations, decay_function):

        if parameter_type_to_modify == "timeframe":
            parameter = random.choice(list(offspring.parameter_dictionary["timeframe"]))

            offspring.parameter_dictionary["timeframe"][parameter] = \
                self.timeframe_gen(offspring.parameter_dictionary["timeframe"][parameter],
                                   current_generation, nb_of_generations, decay_function)

        elif parameter_type_to_modify == "rsi_standard_upper_thresholds":
            parameter = random.choice(list(offspring.parameter_dictionary["rsi_standard_upper_thresholds"]))

            offspring.parameter_dictionary["rsi_standard_upper_thresholds"][parameter] = \
                self.rsi_upper_threshold_gen(
                    offspring.parameter_dictionary["rsi_standard_upper_thresholds"][parameter],
                    current_generation, nb_of_generations, decay_function)

        elif parameter_type_to_modify == "rsi_standard_lower_thresholds":
            parameter = random.choice(list(offspring.parameter_dictionary["rsi_standard_lower_thresholds"]))

            offspring.parameter_dictionary["rsi_standard_lower_thresholds"][parameter] = \
                self.rsi_lower_threshold_gen(
                    offspring.parameter_dictionary["rsi_standard_lower_thresholds"][parameter],
                    current_generation, nb_of_generations, decay_function)

        elif parameter_type_to_modify == "smoothing_factors":
            parameter = random.choice(list(offspring.parameter_dictionary["smoothing_factors"]))

            offspring.parameter_dictionary["smoothing_factors"][parameter] = \
                self.smoothing_factor_gen(offspring.parameter_dictionary["smoothing_factors"][parameter],
                                          current_generation, nb_of_generations, decay_function)

        elif parameter_type_to_modify == "amplification_factors":
            parameter = random.choice(list(offspring.parameter_dictionary["amplification_factors"]))

            offspring.parameter_dictionary["amplification_factors"][parameter] = \
                self.amplification_factor_gen(
                    offspring.parameter_dictionary["amplification_factors"][parameter],
                    current_generation, nb_of_generations, decay_function)

        elif parameter_type_to_modify == "weights":
            parameter = random.choice(list(offspring.parameter_dictionary["weights"]))

            offspring.parameter_dictionary["weights"][parameter] = \
                self.weight_gen(offspring.parameter_dictionary["weights"][parameter],
                                current_generation, nb_of_generations, decay_function)

        elif parameter_type_to_modify == "lwma_max_weights":
            parameter = random.choice(list(offspring.parameter_dictionary["lwma_max_weights"]))

            offspring.parameter_dictionary["lwma_max_weights"][parameter] = \
                self.weight_gen(offspring.parameter_dictionary["lwma_max_weights"][parameter],
                                current_generation, nb_of_generations, decay_function)

        elif parameter_type_to_modify == "major_spline_standard_upper_thresholds":
            parameter = random.choice(list(offspring.parameter_dictionary["major_spline_standard_upper_thresholds"]))

            offspring.parameter_dictionary["major_spline_standard_upper_thresholds"][parameter] = \
                self.major_spline_upper_threshold_gen(
                    offspring.parameter_dictionary["major_spline_standard_upper_thresholds"][parameter],
                    current_generation, nb_of_generations, decay_function)

        elif parameter_type_to_modify == "major_spline_standard_lower_thresholds":
            parameter = random.choice(list(offspring.parameter_dictionary["major_spline_standard_lower_thresholds"]))

            offspring.parameter_dictionary["major_spline_standard_lower_thresholds"][parameter] = \
                self.major_spline_lower_threshold_gen(
                    offspring.parameter_dictionary["major_spline_standard_lower_thresholds"][parameter],
                    current_generation, nb_of_generations, decay_function)

        return offspring

    # ===============================================================================
    # ------- Timeframes
    @staticmethod
    def timeframe_random_gen():
        return random.randint(2, 100)

    @staticmethod
    def timeframe_gen(current_parameter, current_generation, nb_of_generations, decay_function):
        # Throttle variation parameters
        throttled_param = round(EVOA_tools().throttle(current_generation, nb_of_generations,
                                                      6, 1, decay_function))

        # Update parameter using throttled ranges
        new_parameter = current_parameter + random.randint(-throttled_param, throttled_param)

        if new_parameter < 3:
            new_parameter = 2
        return new_parameter

    # ------- Smoothing factors
    @staticmethod
    def smoothing_factor_random_gen():
        return random.uniform(0.0, 2.0)

    @staticmethod
    def smoothing_factor_gen(current_parameter, current_generation, nb_of_generations, decay_function):
        # Throttle variation parameters
        throttled_param = EVOA_tools().throttle(current_generation, nb_of_generations,
                                                1, 0.01, decay_function)

        # Update parameter using throttled ranges
        new_parameter = current_parameter + random.uniform(-throttled_param, throttled_param)

        if new_parameter < 0:
            new_parameter = 0
        return new_parameter

    # ------- Amplification factors
    @staticmethod
    def amplification_factor_random_gen():
        return random.uniform(0.0, 3.0)

    @staticmethod
    def amplification_factor_gen(current_parameter, current_generation, nb_of_generations, decay_function):
        # Throttle variation parameters
        throttled_param = EVOA_tools().throttle(current_generation, nb_of_generations,
                                                1.5, 0.01, decay_function)

        # Update parameter using throttled ranges
        new_parameter = current_parameter + random.uniform(-throttled_param, throttled_param)

        if new_parameter < 0:
            new_parameter = 0
        return new_parameter

    # ------- Weights
    @staticmethod
    def weight_random_gen():
        return random.uniform(0.0, 10.0)

    @staticmethod
    def weight_gen(current_parameter, current_generation, nb_of_generations, decay_function):
        # Throttle variation parameters
        throttled_param = EVOA_tools().throttle(current_generation, nb_of_generations,
                                                4, 0.01, decay_function)

        # Update parameter using throttled ranges
        new_parameter = current_parameter + random.uniform(-throttled_param, throttled_param)

        if new_parameter < 0:
            new_parameter = 0
        return new_parameter

    # ------- LWMA max weight
    @staticmethod
    def lwma_max_weight_random_gen():
        return random.randint(1, 100)

    @staticmethod
    def lwma_max_weight_gen(current_parameter, current_generation, nb_of_generations, decay_function):
        # Throttle variation parameters
        throttled_param = EVOA_tools().throttle(current_generation, nb_of_generations,
                                                50, 1, decay_function)

        # Update parameter using throttled ranges
        new_parameter = current_parameter + random.uniform(-throttled_param, throttled_param)

        if new_parameter < 0:
            new_parameter = 1
        return new_parameter

    # ------- RSI standard Upper/Lower thresholds
    @staticmethod
    def rsi_upper_threshold_random_gen():
        return random.randint(51, 90)

    @staticmethod
    def rsi_lower_threshold_random_gen():
        return random.randint(10, 49)

    @staticmethod
    def rsi_upper_threshold_gen(current_parameter, current_generation, nb_of_generations, decay_function):
        # Throttle variation parameters
        throttled_param = round(EVOA_tools().throttle(current_generation, nb_of_generations,
                                                      20, 1, decay_function))

        # Update parameter using throttled ranges
        new_parameter = current_parameter + random.randint(-throttled_param, throttled_param)

        if new_parameter < 51:
            new_parameter = 51

        if new_parameter > 90:
            new_parameter = 90

        return new_parameter

    @staticmethod
    def rsi_lower_threshold_gen(current_parameter, current_generation, nb_of_generations, decay_function):
        # Throttle variation parameters
        throttled_param = round(EVOA_tools().throttle(current_generation, nb_of_generations,
                                                      20, 1, decay_function))

        # Update parameter using throttled ranges
        new_parameter = current_parameter + random.randint(-throttled_param, throttled_param)

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
    def major_spline_upper_threshold_gen(current_parameter, current_generation, nb_of_generations, decay_function):
        # Throttle variation parameters
        throttled_param = EVOA_tools().throttle(current_generation, nb_of_generations,
                                                0.2, 0.01, decay_function)

        # Update parameter using throttled ranges
        new_parameter = current_parameter + random.uniform(-throttled_param, throttled_param)

        if new_parameter < 0.3:
            new_parameter = 0.3

        if new_parameter > 0.6:
            new_parameter = 0.6

        return new_parameter

    @staticmethod
    def major_spline_lower_threshold_gen(current_parameter, current_generation, nb_of_generations, decay_function):
        # Throttle variation parameters
        throttled_param = EVOA_tools().throttle(current_generation, nb_of_generations,
                                                0.2, 0.01, decay_function)

        # Update parameter using throttled ranges
        new_parameter = current_parameter + random.uniform(-throttled_param, throttled_param)

        if new_parameter > -0.3:
            new_parameter = -0.3

        if new_parameter < -0.6:
            new_parameter = -0.6

        return new_parameter
