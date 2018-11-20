import tkinter as tk
import numpy as np
from tkinter import ttk
from tkinter import N,S,E,W, NO, YES, END, FIRST, LAST, DISABLED, NORMAL, TOP, BOTTOM, LEFT, RIGHT
import sys
from PIL import Image,ImageTk
import time, datetime
import matplotlib

class AcumenApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        """
        Initialization of base class, this is where all pages are managed
        :param args: Tkinter-required args
        :param kwargs: Tkinter-required kwargs
        """
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default='./GUI/icons/main_icon_2.ico')
        tk.Tk.wm_title(self, "Acumen")

        self.resizable(True, True)

        self.width = 900
        self.height = 620
        self.xposition = int(self.winfo_screenwidth() / 2 - self.width / 2)
        self.yposition = int(self.winfo_screenheight() / 2 - self.height / 2)

        self.geometry("{0}x{1}+{2}+{3}".format(self.width, self.height, self.xposition, self.yposition))

        container = tk.Frame(self)
        container.grid(row=0, column=0)

if __name__ == "__main__":

    App = AcumenApp()
    App.geometry("900x750")
    ani = animation.FuncAnimation(F, StatsPage.animate, interval=250)
    App.mainloop()
