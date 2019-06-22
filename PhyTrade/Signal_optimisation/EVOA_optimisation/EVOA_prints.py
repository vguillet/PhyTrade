from PhyTrade.Settings.SETTINGS import SETTINGS
import time


class EVOA_prints:
    def __init__(self, ticker, evoa_version):
        self.settings = SETTINGS()
        self.settings.signal_training_settings.gen_evoa_settings()
        self.settings.metalabeling_settings.gen_metalabels_settings()
        self.settings.individual_settings.gen_individual_settings()

        self.ticker = ticker
        self.evoa_version = evoa_version

        # --> Perform Monkey Patching update of print methods if multiprocessing
        if self.settings.signal_training_settings.multiprocessing:
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

    def evoa_run_initialisation_recap(self):
        # decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("EVOA_v"+str(self.evoa_version), "\n")

        print("Evaluated ticker:", self.ticker)
        print("Start time:", time.strftime('%X %x %Z'), "\n")

        print("-- Settings selected --")
        print("Selected evaluation method:", self.settings.signal_training_settings.evaluation_methods[self.settings.signal_training_settings.evaluation_method])
        print("Selected metalabeling method:", self.settings.metalabeling_settings.metalabeling_settings[self.settings.metalabeling_settings.metalabeling_setting])
        print("")
        print("Selected parent function:", self.settings.signal_training_settings.decay_functions[self.settings.signal_training_settings.parents_decay_function])
        print("Selected random individual function:", self.settings.signal_training_settings.decay_functions[self.settings.signal_training_settings.random_ind_decay_function])
        print("Selected mutation range function:", self.settings.signal_training_settings.decay_functions[self.settings.signal_training_settings.mutation_decay_function])
        print("")
        print("Configuration sheet:", self.settings.signal_training_settings.config_name)
        print("Starting parameters:", self.settings.signal_training_settings.starting_parameters)
        print("")

        if self.settings.signal_training_settings.starting_parameters is None:
            print("Indicators tuned: -> RSI:", self.settings.individual_settings.rsi_count)
            print("                  -> SMA:", self.settings.individual_settings.sma_count)
            print("                  -> EMA:", self.settings.individual_settings.ema_count)
            print("                  -> LWMA:", self.settings.individual_settings.lwma_count)
            print("                  -> CCI:", self.settings.individual_settings.cci_count)
            print("                  -> EVM:", self.settings.individual_settings.eom_count)
            print("                  -> OC gradient:", 1)

        else:
            print("Indicators tuned: -> RSI:", self.settings.signal_training_settings.starting_parameters["indicators_count"]["rsi"])
            print("                  -> SMA:", self.settings.signal_training_settings.starting_parameters["indicators_count"]["sma"])
            print("                  -> EMA:", self.settings.signal_training_settings.starting_parameters["indicators_count"]["ema"])
            print("                  -> LWMA:", self.settings.signal_training_settings.starting_parameters["indicators_count"]["lwma"])
            print("                  -> CCI:", self.settings.signal_training_settings.starting_parameters["indicators_count"]["cci"])
            print("                  -> EVM:", self.settings.signal_training_settings.starting_parameters["indicators_count"]["eom"])
            print("                  -> OC gradient:", 1)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def new_slice_info(self, data_slice, gen, cycle_count):
        print("\n================================= Generation", gen, "/", self.settings.signal_training_settings.nb_of_generations + 1,
              "=================================")
        print("Data slice analysed:", data_slice.start_date, "-->", data_slice.stop_date)
        print("Data slice analysed:", data_slice.start_index, "-->", data_slice.stop_index)
        print("Data slice analysis cycle:", cycle_count, "\n")

    def generation_info(self, gen, generation_start_time, generation_end_time,
                        results, net_worth, fitness_evaluation,
                        population):
        print("\n--", self.ticker, "- Generation", gen + 1, "population evaluation completed --")
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

    @staticmethod
    def end_of_optimisation_msg(total_data_points_processed):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("All data processed")
        print("Number of data points processed:", total_data_points_processed)
        print("Parameter optimisation completed")

        print("\nEnd time:", time.strftime('%X %x %Z'), "\n")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    @staticmethod
    def init_pop_success_msg():
        print("\n---------------> Initial population generated successfully")

    @staticmethod
    def exploration_phase_complete_msg():
        print("\n-------------> Exploration phase completed, starting exploitation phase <-------------")

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
        print("\nParameter sets evolution completed (Darwin put in charge)\n")

    @staticmethod
    def eval_pop_msg():
        print("---------------> Evaluating population")

    @staticmethod
    def invalid_slice_msg():
        print("Data slice invalid for training, proceed to next data slice")
