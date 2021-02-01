
##################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs

# Own modules
from GUI.Tools.Worker_thread import WorkerSignals, Worker

from GUI.ui_connections.Main_settings_c import save_market_settings, save_tradebot_settings
from GUI.ui_connections.EVOA_optimiser_settings_c import save_EVOA_optimiser_settings
from GUI.ui_connections.EVOA_metalabels_settings_c import save_EVOA_metalabels_settings
from GUI.ui_connections.Metalabeling_settings_c import save_simple_metalabels_settings
from GUI.ui_connections.Model_settings_c import save_model_settings
from GUI.ui_connections.Trade_sim_settings_c import save_general_trade_sim_settings, save_single_ticker_trade_sim_settings, save_multi_ticker_trade_sim_settings

from src.RUN_protocols import RUN_protocols

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class UI_connector:
    def __init__(self, ui, threadpool):
        self.ui = ui
        self.threadpool = threadpool

        # --> Batch settings
        ui.batch_save_settings.clicked.connect(self.__save_batch_settings)

        # --> Main settings
        self.ui.main_save_settings.clicked.connect(self.__save_main_settings)

        # --> Optimisers settings
        self.ui.EVOA_optimisation_save_settings.clicked.connect(save_EVOA_optimiser_settings(ui=self.ui,
                                                                                             location="EVOA_optimiser_settings",
                                                                                             name=self.ui.EVOA_optimisation_config_name.text()))
        self.ui.EVOA_optimisation_run.clicked.connect(self.__run_EVOA_optimiser)

        # --> Metalabels settings
        self.ui.EVOA_metalabeling_save_settings.clicked.connect(save_EVOA_metalabels_settings(ui=self.ui,
                                                                                              location="EVOA_metalabels_settings",
                                                                                              name=self.ui.EVOA_metalabeling_config_name.text()))
        self.ui.EVOA_metalabels_run.clicked.connect(self.__run_EVOA_metalabels_gen)

        self.ui.simple_metalabeling_save_settings.clicked.connect(save_simple_metalabels_settings(ui=self.ui,
                                                                                                  location="Simple_metalabels_settings",
                                                                                                  name=self.ui.backtesting_config_name.text()))

        # TODO: Uncomment when simple metalabel added
        # self.ui.simple_metalabels_run.clicked.connect(self.__run_simple_metalabels_gen)

        # --> Economic evaluation
        self.ui.economic_evaluation_run.clicked.connect(self.__run_economic_evaluation_gen)

        # --> Trade sim settings
        self.ui.trade_sim_general_save_settings.clicked.connect(save_general_trade_sim_settings(ui=self.ui,
                                                                                                location="General_trade_sim_settings",
                                                                                                name=self.ui.simulation_name.text()))

        self.ui.stts_save_settings.clicked.connect(save_single_ticker_trade_sim_settings(ui=self.ui,
                                                                                         location="Single_ticker_trade_sim_settings",
                                                                                         name=self.ui.simulation_name.text()))
        self.ui.stts_run.clicked.connect(self.__stts_run)

        self.ui.mtts_save_settings.clicked.connect(save_multi_ticker_trade_sim_settings(ui=self.ui,
                                                                                        location="Multi_ticker_trade_sim_settings",
                                                                                        name=self.ui.simulation_name.text()))
        self.ui.mtts_run.clicked.connect(self.__mtts_run)

    # =======================================================================================================
    # ---------------- Current settings functions
    def __save_current_settings(self):
        # --> Main settings
        save_market_settings(self.ui)
        save_tradebot_settings(self.ui)

        # --> Optimisers settings
        save_EVOA_optimiser_settings(self.ui)

        # --> Metalabels settings
        save_EVOA_metalabels_settings(self.ui)
        save_simple_metalabels_settings(self.ui)

        # --> Economic evaluation
        save_model_settings(self.ui)

        # --> Trade sim settings
        save_general_trade_sim_settings(self.ui)
        save_single_ticker_trade_sim_settings(self.ui)
        save_multi_ticker_trade_sim_settings(self.ui)

        print("Check")

    # ---------------- Batch settings functions
    def __save_batch_settings(self):
        save_market_settings(ui=self.ui,
                             location="Market_settings",
                             name=self.ui.config_name_market.text())

        save_tradebot_settings(ui=self.ui,
                               location="Tradebot_settings",
                               name=self.ui.config_name_tradebot.text())

        save_EVOA_optimiser_settings(ui=self.ui,
                                     location="EVOA_optimiser_settings",
                                     name=self.ui.config_name_1.text())

        save_EVOA_metalabels_settings(ui=self.ui,
                                      location="EVOA_metalabels_settings",
                                      name=self.ui.config_name_2.text())

        save_simple_metalabels_settings(ui=self.ui,
                                        location="Simple_metalabels_settings",
                                        name=self.ui.config_name_2.text())

        save_general_trade_sim_settings(ui=self.ui,
                                        location="General_trade_sim_settings",
                                        name=self.ui.simulation_name.text())

        save_single_ticker_trade_sim_settings(ui=self.ui,
                                              location="Single_ticker_trade_sim_settings",
                                              name=self.ui.simulation_name.text())

        save_multi_ticker_trade_sim_settings(ui=self.ui,
                                             location="Multi_ticker_trade_sim_settings",
                                             name=self.ui.simulation_name.text())

    # ---------------- Main settings functions
    def __save_main_settings(self):
        save_market_settings(ui=self.ui,
                             location="Market_settings",
                             name=self.ui.config_name_market.text())

        save_tradebot_settings(ui=self.ui,
                               location="Tradebot_settings",
                               name=self.ui.config_name_tradebot.text())

    # ---------------- Optimisers settings functions
    def __run_EVOA_optimiser(self):
        # --> Record settings
        self.__save_current_settings()

        # --> Initiate process in thread
        worker = Worker(RUN_protocols(task_sequence=[1]))
        # worker.signals.progress.connect(self.update_gui)

        self.threadpool.start(worker)

    # ---------------- Metalabels settings functions
    # --> EVOA metalabels
    def __run_EVOA_metalabels_gen(self):
        # --> Record settings
        self.__save_current_settings()

        # --> Initiate process in thread
        worker = Worker(RUN_protocols(task_sequence=[2]))
        # worker.signals.progress.connect(self.update_gui)

        self.threadpool.start(worker)

    # --> Simple metalabels
    def __run_simple_metalabels_gen(self):
        # --> Record settings
        self.__save_current_settings()

        # TODO: Add simple metalabel gen

    # ---------------- Economic evaluation functions
    def __run_economic_evaluation_gen(self):
        # --> Record settings
        self.__save_current_settings()

        # --> Initiate process in thread
        worker = Worker(RUN_protocols(task_sequence=[3]))
        # worker.signals.progress.connect(self.update_gui)

        self.threadpool.start(worker)

    # ---------------- Trade sim settings functions
    # --> Single ticker trade simulation
    def __stts_run(self):
        # --> Record settings
        self.__save_current_settings()

        # --> Initiate process in thread
        worker = Worker(RUN_protocols(task_sequence=[4]))
        # worker.signals.progress.connect(self.update_gui)

        self.threadpool.start(worker)

    # --> Multi-ticker trade simulation
    def __mtts_run(self):
        # --> Record settings
        self.__save_current_settings()

        # --> Initiate process in thread
        worker = Worker(RUN_protocols(task_sequence=[5]))
        # worker.signals.progress.connect(self.update_gui)

        self.threadpool.start(worker)
