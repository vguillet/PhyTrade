
##################################################################################################################
"""
pyuic5 -x file.ui -o file.py
"""

# TODO: Add Individual settings gen

# Built-in/Generic Imports
import sys
import json

# Libs
from PyQt5 import QtWidgets, QtGui, QtCore

# Own modules
from GUI_1_1.ui_layouts.Main_window_ui import Ui_mainWindow

from GUI_1_1.ui_connections.Main_settings_c import save_market_settings, save_tradebot_settings
from GUI_1_1.ui_connections.EVOA_optimiser_settings_c import save_EVOA_optimiser_settings
from GUI_1_1.ui_connections.EVOA_metalabels_settings_c import save_EVOA_metalabels_settings
from GUI_1_1.ui_connections.Metalabeling_settings_c import save_simple_metalabels_settings
from GUI_1_1.ui_connections.Model_settings_c import save_model_settings
from GUI_1_1.ui_connections.Trade_sim_settings_c import save_general_trade_sim_settings, save_single_ticker_trade_sim_settings, save_multi_ticker_trade_sim_settings

from PhyTrade.Tools.RUN_protocols import RUN_protocols

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

##################################################################################################################


class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        # --> Set settings mode to 1 to use file based settings
        with open(r"C:\Users\Victor Guillet\Google Drive\Computer science\2-Programing\Repos\Python\Steffegium\Settings\settings_mode.json", 'w') as fout:
            json.dump(1, fout, indent=4)

        super(mywindow, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        # --> Main settings
        # --> Batch settings
        self.ui.batch_save_settings.clicked.connect(self.__save_batch_settings)

        # --> Main settings
        self.ui.main_save_settings.clicked.connect(self.__save_main_settings)

        # --> Optimisers settings
        self.ui.EVOA_optimisation_save_settings.clicked.connect(
            save_EVOA_optimiser_settings(self.ui, location="EVOA_optimiser_settings", name=self.ui.config_name_1.text()))
        self.ui.EVOA_optimisation_run.clicked.connect(self.__run_EVOA_optimiser)

        # --> Metalabels settings
        self.ui.EVOA_metalabeling_save_settings.clicked.connect(
            save_EVOA_metalabels_settings(self.ui, location="EVOA_metalabels_settings", name=self.ui.config_name_2.text()))
        self.ui.EVOA_metalabels_run.clicked.connect(self.__run_EVOA_metalabels_gen)

        self.ui.simple_metalabeling_save_settings.clicked.connect(
            save_simple_metalabels_settings(self.ui, location="Simple_metalabels_settings", name=self.ui.config_name_2.text()))

        # TODO: Uncomment when simple metalabel added
        # self.ui.simple_metalabels_run.clicked.connect(self.__run_simple_metalabels_gen)

        # --> Economic evaluation
        self.ui.economic_evaluation_run.clicked.connect(self.__run_economic_evaluation_gen)

        # --> Trade sim settings
        self.ui.trade_sim_general_save_settings.clicked.connect(
            save_general_trade_sim_settings(self.ui, location="General_trade_sim_settings", name=self.ui.simulation_name.text()))

        self.ui.stts_save_settings.clicked.connect(
            save_single_ticker_trade_sim_settings(self.ui, location="Single_ticker_trade_sim_settings", name=self.ui.simulation_name.text()))
        self.ui.stts_run.clicked.connect(self.__stts_run)

        self.ui.mtts_save_settings.clicked.connect(
            save_multi_ticker_trade_sim_settings(self.ui, location="Multi_ticker_trade_sim_settings", name=self.ui.simulation_name.text()))
        self.ui.mtts_run.clicked.connect(self.__mtts_run)

    # =======================================================================================================================
    # ---------------- Main settings functions
    # --> Batch
    def __save_batch_settings(self):
        save_market_settings(self.ui, location="Market_settings", name=self.ui.config_name_market.text())
        save_tradebot_settings(self.ui, location="Tradebot_settings", name=self.ui.config_name_tradebot.text())
        save_EVOA_optimiser_settings(self.ui, location="EVOA_optimiser_settings", name=self.ui.config_name_1.text())
        save_EVOA_metalabels_settings(self.ui, location="EVOA_metalabels_settings", name=self.ui.config_name_2.text())
        save_simple_metalabels_settings(self.ui, location="Simple_metalabels_settings", name=self.ui.config_name_2.text())
        save_general_trade_sim_settings(self.ui, location="General_trade_sim_settings", name=self.ui.simulation_name.text())
        save_single_ticker_trade_sim_settings(self.ui, location="Single_ticker_trade_sim_settings", name=self.ui.simulation_name.text())
        save_multi_ticker_trade_sim_settings(self.ui, location="Multi_ticker_trade_sim_settings", name=self.ui.simulation_name.text())

    # --> Main
    def __save_main_settings(self):
        save_market_settings(self.ui, location="Market_settings", name=self.ui.config_name_market.text())
        save_tradebot_settings(self.ui, location="Tradebot_settings", name=self.ui.config_name_tradebot.text())

    # ---------------- Optimisers settings functions
    def __run_EVOA_optimiser(self):
        self.__save_current_settings()
        RUN_protocols([1])

    # ---------------- Metalabels settings functions
    # --> EVOA metalabels
    def __run_EVOA_metalabels_gen(self):
        self.__save_current_settings()
        RUN_protocols([2])

    # --> Simple metalabels
    def __run_simple_metalabels_gen(self):
        self.__save_current_settings()

    # ---------------- Economic evaluation functions
    def __run_economic_evaluation_gen(self):
        self.__save_current_settings()
        RUN_protocols([3])

    # ---------------- Trade sim settings functions
    # --> General

    # --> stts
    def __stts_run(self):
        self.__save_current_settings()
        RUN_protocols([4])

    # --> mtts
    def __mtts_run(self):
        self.__save_current_settings()
        RUN_protocols([5])

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


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    application = mywindow()

    application.show()

    sys.exit(app.exec())
