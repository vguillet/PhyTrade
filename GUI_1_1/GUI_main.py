
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import sys

# Libs
from PyQt5 import QtWidgets, QtGui, QtCore

# Own modules
from GUI_1_1.ui_layouts.Main_window_ui import Ui_mainWindow

from GUI_1_1.ui_connections.Main_settings_c import get_market_settings, get_tradebot_settings
from GUI_1_1.ui_connections.EVOA_optimiser_settings_c import get_EVOA_optimiser_settings
from GUI_1_1.ui_connections.EVOA_metalabels_settings_c import get_EVOA_metalabels_settings
from GUI_1_1.ui_connections.Metalabeling_settings_c import get_simple_metalabels_settings
from GUI_1_1.ui_connections.Model_settings_c import get_model_settings

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

##################################################################################################################


class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.ui.EVOA_optimisation_run.clicked.connect(self.__run_EVOA_optimiser)
        self.ui.EVOA_metalabels_run.clicked.connect(self.__run_EVOA_metalabels_gen)
        self.ui.simple_metalabels_run.clicked.connect(self.__run_simple_metalabels_gen)
        self.ui.economic_evaluation_run.clicked.connect(self.__run_economic_evaluation_gen)

    def __run_EVOA_optimiser(self):
        get_market_settings(self.ui)
        get_tradebot_settings(self.ui)

        get_EVOA_optimiser_settings(self.ui)

    def __run_EVOA_metalabels_gen(self):
        get_market_settings(self.ui)
        get_tradebot_settings(self.ui)

        get_EVOA_metalabels_settings(self.ui)

    def __run_simple_metalabels_gen(self):
        get_market_settings(self.ui)
        get_tradebot_settings(self.ui)

        get_simple_metalabels_settings(self.ui)

    def __run_economic_evaluation_gen(self):
        get_market_settings(self.ui)
        get_tradebot_settings(self.ui)

        get_model_settings(self.ui)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    application = mywindow()

    application.show()

    sys.exit(app.exec())