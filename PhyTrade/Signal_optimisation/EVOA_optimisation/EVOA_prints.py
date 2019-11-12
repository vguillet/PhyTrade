
################################################################################################################
"""
Contains all the prints function used by the EVOA optimiser algorithm.
Also contains a monkey patch for removing prints in case of multiprocessing
"""

# Libs
import time

# Own modules
from PhyTrade.Tools.Colours_and_Fonts import cf

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class EVOA_prints:
    def __init__(self, ticker, evoa_version, settings):
        self.settings = settings
        self.settings.individual_settings.gen_individual_settings()

        self.ticker = ticker
        self.evoa_version = evoa_version

        # --> Perform Monkey Patching update of print methods if multiprocessing
        if self.settings.signal_training_settings.multiprocessing:
            self.evoa_settings_auto_adjust = self.monkey_patch_pass
            self.evoa_run_initialisation_recap = self.monkey_patch_pass
            self.new_slice_info = self.monkey_patch_pass
            self.generation_info = self.monkey_patch_pass
            self.end_of_optimisation_msg = self.monkey_patch_pass
            self.init_pop_success_msg = self.monkey_patch_pass
            self.exploration_phase_complete_msg = self.monkey_patch_pass
            self.det_new_generation_param_msg = self.monkey_patch_pass
            self.select_ind_msg = self.monkey_patch_pass
            self.gen_offsprings_msg = self.monkey_patch_pass
            self.darwin_in_charge_msg = self.monkey_patch_pass
            self.eval_pop_msg = self.monkey_patch_pass
            self.invalid_slice_msg = self.monkey_patch_pass

    @staticmethod
    def monkey_patch_pass(*args, **kwargs):
        return

    def evoa_run_initialisation_recap(self, run_mode, slice_count, generation_count):
        # decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        print(cf["green"] + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + cf["reset"])
        print(cf["bold"] + "EVOA_v"+str(self.evoa_version) + cf["reset"], "\n")

        if run_mode == 1:
            print("RUN Mode: " + cf["green"] + "Signal tuner" + cf["reset"])
            print("\nNumber of data slices to be processed:", slice_count)
            print("--> Generation count updated to", generation_count, "to match available data <--\n")

        elif run_mode == 2:
            print("RUN Mode: " + cf["green"] + "Optimiser" + cf["reset"])
            print("\nGeneration count:", generation_count, "\n")

        print("Evaluated ticker: " + cf["green"] + self.ticker + cf["reset"])
        print("Start time: " + cf["green"] + str(time.strftime('%X %x %Z')) + cf["reset"], "\n")

        print("-- Settings selected --")
        print("Selected evaluation method: " + cf["green"] + self.settings.signal_training_settings.evaluation_methods[self.settings.signal_training_settings.evaluation_method] + cf["reset"])
        print("Labeling method: " + cf["green"] + self.settings.metalabeling_settings.metalabeling_settings[self.settings.metalabeling_settings.metalabeling_setting] + cf["reset"])
        print("")
        print("Selected parent function: " + cf["green"] + self.settings.signal_training_settings.decay_functions[self.settings.signal_training_settings.parents_decay_function] + cf["reset"])
        print("Selected random individual function: " + cf["green"] + self.settings.signal_training_settings.decay_functions[self.settings.signal_training_settings.random_ind_decay_function] + cf["reset"])
        print("Selected mutation range function: " + cf["green"] + self.settings.signal_training_settings.decay_functions[self.settings.signal_training_settings.mutation_decay_function] + cf["reset"])
        print("")
        print("Configuration sheet: " + cf["green"] + self.settings.signal_training_settings.config_name + cf["reset"])
        print("Starting parameters: " + cf["green"] + str(self.settings.signal_training_settings.starting_parameters) + cf["reset"])
        print("")

        if self.settings.signal_training_settings.starting_parameters is None:
            print("Indicators tuned: -> RSI: " + cf["green"] + str(self.settings.individual_settings.rsi_count) + cf["reset"])
            print("                  -> SMA: " + cf["green"] + str(self.settings.individual_settings.sma_count) + cf["reset"])
            print("                  -> EMA: " + cf["green"] + str(self.settings.individual_settings.ema_count) + cf["reset"])
            print("                  -> LWMA: " + cf["green"] + str(self.settings.individual_settings.lwma_count) + cf["reset"])
            print("                  -> CCI: " + cf["green"] + str(self.settings.individual_settings.cci_count) + cf["reset"])
            print("                  -> EVM: " + cf["green"] + str(self.settings.individual_settings.eom_count) + cf["reset"])
            print("                  -> OC gradient: " + cf["green"] + str(1) + cf["reset"])

        else:
            print("Indicators tuned: -> RSI: " + cf["green"] + str(self.settings.signal_training_settings.starting_parameters["indicators_count"]["rsi"]) + cf["reset"])
            print("                  -> SMA: " + cf["green"] + str(self.settings.signal_training_settings.starting_parameters["indicators_count"]["sma"]) + cf["reset"])
            print("                  -> EMA: " + cf["green"] + str(self.settings.signal_training_settings.starting_parameters["indicators_count"]["ema"]) + cf["reset"])
            print("                  -> LWMA: " + cf["green"] + str(self.settings.signal_training_settings.starting_parameters["indicators_count"]["lwma"]) + cf["reset"])
            print("                  -> CCI: " + cf["green"] + str(self.settings.signal_training_settings.starting_parameters["indicators_count"]["cci"]) + cf["reset"])
            print("                  -> EVM: " + cf["green"] + str(self.settings.signal_training_settings.starting_parameters["indicators_count"]["eom"]) + cf["reset"])
            print("                  -> OC gradient: " + cf["green"] + str(1) + cf["reset"])
        print(cf["green"] + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" + cf["reset"])

    def generation_info(self, gen, generation_start_time, generation_end_time,
                        results, net_worth, fitness_evaluation,
                        population):
        print("\n--", self.ticker, "- Generation", gen, "population evaluation completed --")
        print("Total generation Run time:", round(generation_end_time - generation_start_time, 3), "s")

        print("\nMetalabel net worth:", round(results.data_slice_metalabel_pp[-1], 3))
        print("Average net worth:", round((sum(net_worth) / len(net_worth)), 3))

        print("\n-> Best individual:")
        index_best_individual = fitness_evaluation.index(max(fitness_evaluation))

        print("Net worth:", round(net_worth[index_best_individual], 3))
        print("Transaction count:", population[index_best_individual].tradebot.buy_count +
              population[index_best_individual].tradebot.sell_count)
        print("Buy count:", population[index_best_individual].tradebot.buy_count)
        print("Sell count:", population[index_best_individual].tradebot.sell_count)

        print("\nBest Individual fitness:", round(max(fitness_evaluation), 3))
        print("Average fitness:", round((sum(fitness_evaluation) / len(fitness_evaluation)), 3), "\n")

    def new_slice_info(self, data_slice, gen, max_gen, cycle_count):
        print(cf["bold"] + cf["cyan"] + "\n================================= " + cf["reset"] +
              "Generation " + str(gen) + cf["bold"] + cf["cyan"] + "/" + cf["reset"] + str(max_gen) +
              cf["bold"] + cf["cyan"] + " =================================" + cf["reset"])
        print("Data slice analysed:", data_slice.start_date, "-->", data_slice.stop_date)
        print("Data slice analysed:", data_slice.start_index, "-->", data_slice.stop_index)

        if self.settings.signal_training_settings.optimiser_setting == 1:
            print("Data slice analysis cycle:", cycle_count, "\n")
        else:
            print("\n")

    @staticmethod
    def end_of_optimisation_msg(total_data_points_processed):
        print(cf["green"] + "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("All data processed")
        print("Number of data points processed:", total_data_points_processed)
        print("Parameter optimisation completed")

        print("\nEnd time:", time.strftime('%X %x %Z'), "\n")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" + cf["reset"])

    @staticmethod
    def init_pop_success_msg():
        print("\n---------------> Initial population generated successfully")

    @staticmethod
    def exploration_phase_complete_msg():
        print(cf["red"] + "\n------------> Exploration phase completed, starting exploitation phase <------------" + cf["reset"])

    @staticmethod
    def det_new_generation_param_msg():
        print("---------------> Determining new generation parameters")

    @staticmethod
    def select_ind_msg():
        print("---------------> Selecting individuals from previous generation")

    @staticmethod
    def gen_offsprings_msg():
        print("---------------> Generating offsprings with mutations")

    @staticmethod
    def darwin_in_charge_msg():
        print(cf["green"] + "\nParameter sets evolution completed (Darwin put in charge)\n" + cf["reset"])

    @staticmethod
    def eval_pop_msg():
        print("---------------> Evaluating population")

    @staticmethod
    def invalid_slice_msg():
        print("Data slice invalid for training, proceed to next data slice")
