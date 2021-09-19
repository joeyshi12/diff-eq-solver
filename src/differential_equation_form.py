from abc import abstractmethod
from tkinter import Frame

import src.tkinter_config as config


class DifferentialEquationForm(Frame):
    data_folder_path: str = "./data"

    def __init__(self, frame, fig, canvas):
        Frame.__init__(self, master=frame)
        self.fig = fig
        self.canvas = canvas
        self.initialize_widgets()
        self.configure(background=config.details_background)

    def show(self):
        self.lift()

    @abstractmethod
    def initialize_widgets(self):
        raise NotImplementedError
