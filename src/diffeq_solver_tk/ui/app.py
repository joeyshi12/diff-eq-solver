import tkinter as tk

from diffeq_solver_tk.ui.form_container import FormContainer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class App(tk.Frame):
    def __init__(self, master: tk.Tk):
        tk.Frame.__init__(self, master=master)
        figure = Figure(figsize=(6, 1), dpi=91.4)
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().pack(side="right", fill="both", expand=True)
        FormContainer(self, canvas).pack(side="left", fill="both")

