
##################################################################################################################
"""
pyuic5 -x file.ui -o file.py
"""

# TODO: Add Individual settings gen

# Built-in/Generic Imports
import sys
import traceback
import time
import json

# Libs
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QIcon
# from PyQt5.QtWebEngineWidgets import QWebEngineView

# Own modules
# from GUI.Tools.Worker_thread import WorkerSignals, Worker
from GUI.ui_elements.Console_gui import Console_GUI
from GUI.ui_connections.ui_connector import UI_connector

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

##################################################################################################################


class Phytrade_GUI:
    def __init__(self):
        # --> Set settings mode to 1 to use file based settings
        with open(r"Settings/settings_mode.json", 'w') as fout:
            json.dump(1, fout, indent=4)

        # ============================== Initiate QUI
        app = QtWidgets.QApplication([])

        # --> Load Phytrade GUI layout
        self.ui = uic.loadUi("GUI/Layouts/main_page.ui")

        # ============================== Initiate threadpool and workers
        # --> Setting up thread pool
        self.threadpool = QThreadPool()
        
        # ============================== Initiate UI elements
        # --> Load gui element
        self.console_gui = Console_GUI()
        
        # ============================== Initialise console
        # --> Reset log
        self.console_gui.reset_log()

        # --> Initiate console observer
        # worker = Worker(self.update_console)
        # self.threadpool.start(worker)

        # ============================== Initiate ui connections
        UI_connector(self.ui, self.threadpool)

        # ============================== Display GUI
        self.ui.show()

        print("\n - Phytrade Initialisation: Success \n")

        sys.exit(app.exec())

    # =======================================================================================================
    def update_console(self, progress_callback):
        while True:
            time.sleep(0.01)
            self.console_gui.log_console_output()
            self.console_gui.update_console_output(self.ui)


# =======================================================================================================
class WorkerSignals(QObject):
    """"
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    """

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal()


class Worker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done