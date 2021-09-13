from abc import abstractmethod
from tkinter import Frame


class DifferentialEquationForm(Frame):
    data_folder_path = "./data"
    font = ("Verdana", 10)

    def __init__(self, main_view):
        Frame.__init__(self, main_view)
        self.fig = main_view.figure
        self.canvas = main_view.canvas
        self.bgcolour = main_view.bgcolour
        self.root = main_view
        self.initialize_widgets()
        self.configure(background=self.bgcolour)

    def show(self):
        self.clear_form()
        self.lift()

    @abstractmethod
    def initialize_widgets(self):
        raise NotImplementedError

    @abstractmethod
    def clear_form(self):
        raise NotImplementedError
