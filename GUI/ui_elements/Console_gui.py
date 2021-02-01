
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import sys

# Libs
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from qimage2ndarray import array2qimage

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '26/04/2020'

##################################################################################################################


class Console_GUI:
    @staticmethod
    def reset_log():
        with open("GUI/Cache/message.log", 'w') as file:
            # --> Output logfile content to gui
            file.write("")

            file.close()
        return

    @staticmethod
    def log_console_output():
        # --> Create the log file
        log_file = open("GUI/Cache/message.log", "a")
        sys.stdout = log_file

        return

    @staticmethod
    def update_console_output(ui):
        with open("GUI/Cache/message.log", 'r') as file:
            # --> Output logfile content to gui
            text = file.read()
            ui.console_output.setText(text)

        return
