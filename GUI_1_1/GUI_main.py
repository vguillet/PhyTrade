
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import sys

# Libs
from PyQt5 import QtWidgets, QtGui, QtCore

# Own modules
from GUI_1_1.ui_layouts.Main_window_ui import Ui_mainWindow

from GUI_1_1.ui_connections.Market_settings_c import get_main_settings
from GUI_1_1.ui_connections.EVOA_optimiser_settings_c import get_EVOA_optimiser_settings
from GUI_1_1.ui_connections.EVOA_metalabels_settings import get_EVOA_metalabels_settings

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

    def __run_EVOA_optimiser(self):
        get_main_settings(self.ui)
        get_EVOA_optimiser_settings(self.ui)

    def __run_EVOA_metalabels_gen(self):
        get_main_settings(self.ui)
        get_EVOA_metalabels_settings(self.ui)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    application = mywindow()

    application.show()

    sys.exit(app.exec())