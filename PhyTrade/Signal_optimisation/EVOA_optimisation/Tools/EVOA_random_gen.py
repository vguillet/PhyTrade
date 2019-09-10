
##################################################################################################################
"""
Used to generate random values for specific cases
"""

# Built-in/Generic Imports
import random

# Own modules
from PhyTrade.Signal_optimisation.EVOA_optimisation.Tools.EVOA_tools import EVOA_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class EVOA_random_gen:

    def modify_param(self, offspring, parameter_type_to_modify,
                     current_generation, nb_of_generations,
                     current_slice_cycle, nb_of_slice_cycles,
                     decay_function):

        if parameter_type_to_modify == "timeframes":
            parameter = random.choice(list(offspring.parameter_dictionary["indicator_properties"]["timeframes"]))

            offspring.parameter_dictionary["indicator_properties"]["timeframes"][parameter] = \
                self.timeframe_gen(offspring.parameter_dictionary["indicator_properties"]["timeframes"][parameter],
                                   current_generation, nb_of_generations, current_slice_cycle, nb_of_slice_cycles, decay_function)

        elif parameter_type_to_modify == "rsi_standard_upper_thresholds":
            parameter = random.choice(list(offspring.parameter_dictionary["indicator_properties"]["rsi_standard_upper_thresholds"]))

            offspring.parameter_dictionary["indicator_properties"]["rsi_standard_upper_thresholds"][parameter] = \
                self.rsi_upper_threshold_gen(
                    offspring.parameter_dictionary["indicator_properties"]["rsi_standard_upper_thresholds"][parameter],
                    current_generation, nb_of_generations, current_slice_cycle, nb_of_slice_cycles, decay_function)

        elif parameter_type_to_modify == "rsi_standard_lower_thresholds":
            parameter = random.choice(list(offspring.parameter_dictionary["indicator_properties"]["rsi_standard_lower_thresholds"]))

            offspring.parameter_dictionary["indicator_properties"]["rsi_standard_lower_thresholds"][parameter] = \
                self.rsi_lower_threshold_gen(
                    offspring.parameter_dictionary["indicator_properties"]["rsi_standard_lower_thresholds"][parameter],
                    current_generation, nb_of_generations, current_slice_cycle, nb_of_slice_cycles, decay_function)

        elif parameter_type_to_modify == "lwma_max_weights":
            parameter = random.choice(list(offspring.parameter_dictionary["indicator_properties"]["lwma_max_weights"]))

            offspring.parameter_dictionary["indicator_properties"]["lwma_max_weights"][parameter] = \
                self.lwma_max_weight_gen(offspring.parameter_dictionary["indicator_properties"]["lwma_max_weights"][parameter],
                                         current_generation, nb_of_generations, current_slice_cycle, nb_of_slice_cycles, decay_function)

        elif parameter_type_to_modify == "smoothing_factors":
            parameter = random.choice(list(offspring.parameter_dictionary["spline_property"]["smoothing_factors"]))

            offspring.parameter_dictionary["spline_property"]["smoothing_factors"][parameter] = \
                self.smoothing_factor_gen(offspring.parameter_dictionary["spline_property"]["smoothing_factors"][parameter],
                                          current_generation, nb_of_generations, current_slice_cycle, nb_of_slice_cycles, decay_function)

        elif parameter_type_to_modify == "amplification_factors":
            parameter = random.choice(list(offspring.parameter_dictionary["spline_property"]["amplification_factors"]))

            offspring.parameter_dictionary["spline_property"]["amplification_factors"][parameter] = \
                self.amplification_factor_gen(
                    offspring.parameter_dictionary["spline_property"]["amplification_factors"][parameter],
                    current_generation, nb_of_generations, current_slice_cycle, nb_of_slice_cycles, decay_function)

        elif parameter_type_to_modify == "weights":
            parameter = random.choice(list(offspring.parameter_dictionary["spline_property"]["weights"]))

            offspring.parameter_dictionary["spline_property"]["weights"][parameter] = \
                self.weight_gen(offspring.parameter_dictionary["spline_property"]["weights"][parameter],
                                current_generation, nb_of_generations, current_slice_cycle, nb_of_slice_cycles, decay_function)

        elif parameter_type_to_modify == "major_spline_standard_upper_thresholds":
            offspring.parameter_dictionary["spline_property"]["major_spline_standard_upper_thresholds"] = \
                self.major_spline_upper_threshold_gen(
                    offspring.parameter_dictionary["spline_property"]["major_spline_standard_upper_thresholds"],
                    current_generation, nb_of_generations, current_slice_cycle, nb_of_slice_cycles, decay_function)

        elif parameter_type_to_modify == "major_spline_standard_lower_thresholds":
            offspring.parameter_dictionary["spline_property"]["major_spline_standard_lower_thresholds"] = \
                self.major_spline_lower_threshold_gen(
                    offspring.parameter_dictionary["spline_property"]["major_spline_standard_lower_thresholds"],
                    current_generation, nb_of_generations, current_slice_cycle, nb_of_slice_cycles, decay_function)

        elif parameter_type_to_modify == "flip":
            parameter = random.choice(list(offspring.parameter_dictionary["spline_property"]["flip"]))
            offspring.parameter_dictionary["spline_property"]["flip"][parameter] = self.flip_gen()

        return offspring

    # ===============================================================================
    # ------- Timeframes
    @staticmethod
    def timeframe_random_gen():
        return random.randint(2, 250)

    @staticmethod
    def large_timeframe_random_gen():
        return random.randint(150, 250)

    @staticmethod
    def small_timeframe_random_gen():
        return random.randint(2, 100)

    @staticmethod
    def timeframe_gen(current_parameter,
                      current_generation, nb_of_generations,
                      current_slice_cycle, nb_of_slice_cycles,
                      decay_function):
        
        # Throttle variation parameters according to generation
        throttled_param = round(EVOA_tools().throttle(current_generation, nb_of_generations,
                                                      30, 1, decay_function))
        # Throttle variation parameters according to slice cycle
        throttled_param = round(EVOA_tools().throttle(current_slice_cycle, nb_of_slice_cycles,
                                                      throttled_param, 1, decay_function))

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
    def smoothing_factor_gen(current_parameter,
                             current_generation, nb_of_generations,
                             current_slice_cycle, nb_of_slice_cycles,
                             decay_function):

        # Throttle variation parameters according to generation
        throttled_param = EVOA_tools().throttle(current_generation, nb_of_generations,
                                                1, 0.01, decay_function)
        # Throttle variation parameters according to slice cycle
        throttled_param = EVOA_tools().throttle(current_slice_cycle, nb_of_slice_cycles,
                                                throttled_param, 1, decay_function)

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
    def amplification_factor_gen(current_parameter,
                                 current_generation, nb_of_generations,
                                 current_slice_cycle, nb_of_slice_cycles,
                                 decay_function):

        # Throttle variation parameters according to generation
        throttled_param = EVOA_tools().throttle(current_generation, nb_of_generations,
                                                1.5, 0.01, decay_function)
        # Throttle variation parameters according to slice cycle
        throttled_param = EVOA_tools().throttle(current_slice_cycle, nb_of_slice_cycles,
                                                throttled_param, 0.01, decay_function)

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
    def weight_gen(current_parameter,
                   current_generation, nb_of_generations,
                   current_slice_cycle, nb_of_slice_cycles,
                   decay_function):

        # Throttle variation parameters according to generation
        throttled_param = EVOA_tools().throttle(current_generation, nb_of_generations,
                                                4, 0.01, decay_function)
        # Throttle variation parameters according to slice cycle
        throttled_param = EVOA_tools().throttle(current_slice_cycle, nb_of_slice_cycles,
                                                throttled_param, 0.01, decay_function)
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
    def lwma_max_weight_gen(current_parameter,
                            current_generation, nb_of_generations,
                            current_slice_cycle, nb_of_slice_cycles,
                            decay_function):

        # Throttle variation parameters according to generation
        throttled_param = EVOA_tools().throttle(current_generation, nb_of_generations,
                                                50, 1, decay_function)
        # Throttle variation parameters according to slice cycle
        throttled_param = EVOA_tools().throttle(current_slice_cycle, nb_of_slice_cycles,
                                                throttled_param, 1, decay_function)

        # Update parameter using throttled ranges
        new_parameter = current_parameter + random.uniform(-throttled_param, throttled_param)

        if new_parameter < 1:
            new_parameter = 1

        return new_parameter

    # ------- RSI standard Upper/Lower thresholds
    @staticmethod
    def rsi_upper_threshold_random_gen():
        return random.randint(51, 90)

    @staticmethod
    def rsi_upper_threshold_gen(current_parameter,
                                current_generation, nb_of_generations,
                                current_slice_cycle, nb_of_slice_cycles,
                                decay_function):

        # Throttle variation parameters according to generation
        throttled_param = round(EVOA_tools().throttle(current_generation, nb_of_generations,
                                                      20, 1, decay_function))
        # Throttle variation parameters according to generation
        throttled_param = round(EVOA_tools().throttle(current_slice_cycle, nb_of_slice_cycles,
                                                      throttled_param, 1, decay_function))

        # Update parameter using throttled ranges
        new_parameter = current_parameter + random.randint(-throttled_param, throttled_param)

        if new_parameter < 51:
            new_parameter = 51

        if new_parameter > 90:
            new_parameter = 90

        return new_parameter

    @staticmethod
    def rsi_lower_threshold_random_gen():
        return random.randint(10, 49)

    @staticmethod
    def rsi_lower_threshold_gen(current_parameter,
                                current_generation, nb_of_generations,
                                current_slice_cycle, nb_of_slice_cycles,
                                decay_function):

        # Throttle variation parameters according to generation
        throttled_param = round(EVOA_tools().throttle(current_generation, nb_of_generations,
                                                      20, 1, decay_function))
        # Throttle variation parameters according to generation
        throttled_param = round(EVOA_tools().throttle(current_slice_cycle, nb_of_slice_cycles,
                                                      throttled_param, 1, decay_function))

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
    def major_spline_upper_threshold_gen(current_parameter,
                                         current_generation, nb_of_generations,
                                         current_slice_cycle, nb_of_slice_cycles,
                                         decay_function):

        # Throttle variation parameters according to generation
        throttled_param = EVOA_tools().throttle(current_generation, nb_of_generations,
                                                0.2, 0.01, decay_function)
        # Throttle variation parameters according to generation
        throttled_param = EVOA_tools().throttle(current_slice_cycle, nb_of_slice_cycles,
                                                throttled_param, 0.01, decay_function)

        # Update parameter using throttled ranges
        new_parameter = current_parameter + random.uniform(-throttled_param, throttled_param)

        if new_parameter < 0.3:
            new_parameter = 0.3

        if new_parameter > 0.6:
            new_parameter = 0.6

        return new_parameter

    @staticmethod
    def major_spline_lower_threshold_random_gen():
        return random.uniform(-0.3, -0.6)

    @staticmethod
    def major_spline_lower_threshold_gen(current_parameter,
                                         current_generation, nb_of_generations,
                                         current_slice_cycle, nb_of_slice_cycles,
                                         decay_function):

        # Throttle variation parameters according to generation
        throttled_param = EVOA_tools().throttle(current_generation, nb_of_generations,
                                                0.2, 0.01, decay_function)
        # Throttle variation parameters according to generation
        throttled_param = EVOA_tools().throttle(current_slice_cycle, nb_of_slice_cycles,
                                                throttled_param, 0.01, decay_function)

        # Update parameter using throttled ranges
        new_parameter = current_parameter + random.uniform(-throttled_param, throttled_param)

        if new_parameter > -0.3:
            new_parameter = -0.3

        if new_parameter < -0.6:
            new_parameter = -0.6

        return new_parameter

    @staticmethod
    def flip_random_gen():
        # return bool(random.getrandbits(1))
        return False

    @staticmethod
    def flip_gen():
        return bool(random.getrandbits(1))
