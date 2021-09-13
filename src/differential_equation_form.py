from abc import abstractmethod
from tkinter import Frame, Entry, Label


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
        self.lift()

    @abstractmethod
    def initialize_widgets(self):
        raise NotImplementedError

    def create_field_entry(self, display_name: str, symbol_name: str, row: int):
        field_entry = Entry(self, font=self.font)
        Label(self, text=f"{display_name}:", font=self.font, background=self.bgcolour).grid(
            row=row, column=0, padx=18, pady=10, sticky="w")
        Label(self, text=f"{symbol_name} = ", font=self.font, background=self.bgcolour).grid(
            row=row, column=1, padx=0, pady=10, sticky="e")
        field_entry.grid(row=row, column=2, pady=0)
        return field_entry
