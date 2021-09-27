from abc import abstractmethod
from tkinter import Frame

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import src.tkinter_config as config


class DifferentialEquationForm(Frame):
    data_folder_path: str = "./data"
    canvas: FigureCanvasTkAgg

    def __init__(self, frame, canvas):
        Frame.__init__(self, master=frame)
        self.canvas = canvas
        self.build_form()
        self.configure(background=config.details_background)

    @abstractmethod
    def build_form(self):
        raise NotImplementedError

    @abstractmethod
    def reset(self):
        raise NotImplementedError
