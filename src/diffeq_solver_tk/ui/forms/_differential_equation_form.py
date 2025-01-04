import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter.filedialog import asksaveasfilename

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from diffeq_solver_tk.ui.messages import common_messages
from diffeq_solver_tk.diffeq import DifferentialEquationService


class DifferentialEquationForm(tk.Frame):
    canvas: FigureCanvasTkAgg
    equation_service: DifferentialEquationService

    def __init__(self, master: tk.Frame, canvas: FigureCanvasTkAgg, equation_service: DifferentialEquationService):
        tk.Frame.__init__(self, master=master, padx=18, pady=6)
        self.canvas = canvas
        self.equation_service = equation_service

    def solve_equation(self):
        try:
            metadata = self.get_equation_metadata()
            self.equation_service.compute_and_update_solution(metadata)
            self.on_solve()
            self.canvas.draw()
        except Exception as err:
            showinfo(common_messages.app_name, str(err))

    def export_solution(self):
        table_path = asksaveasfilename(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
        if table_path:
            self.equation_service.export_solution(table_path)

    def get_equation_metadata(self):
        raise NotImplementedError

    def on_solve(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError
