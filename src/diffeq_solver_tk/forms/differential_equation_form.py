from abc import abstractmethod
from tkinter import Frame, messagebox
from tkinter.filedialog import asksaveasfilename

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import diffeq_solver_tk.messages.common_messages as common_messages
import diffeq_solver_tk.tkinter_config as config
from diffeq_solver_tk.services.differential_equation_service import DifferentialEquationService


class DifferentialEquationForm(Frame):
    canvas: FigureCanvasTkAgg
    equation_service: DifferentialEquationService

    def __init__(self, frame: Frame, canvas: FigureCanvasTkAgg, equation_service: DifferentialEquationService):
        Frame.__init__(self, master=frame)
        self.canvas = canvas
        self.equation_service = equation_service
        self.build_form()
        self.configure(background=config.details_background)

    def solve_equation(self):
        try:
            metadata = self.get_equation_metadata()
            self.equation_service.compute_and_update_solution(metadata)
            self.on_solve()
            self.canvas.draw()
        except Exception as err:
            messagebox.showinfo(common_messages.app_name, err)

    def export_solution(self):
        table_path = asksaveasfilename(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
        if table_path:
            self.equation_service.export_solution(table_path)

    @abstractmethod
    def get_equation_metadata(self):
        raise NotImplementedError

    @abstractmethod
    def on_solve(self):
        raise NotImplementedError

    @abstractmethod
    def build_form(self):
        raise NotImplementedError

    @abstractmethod
    def reset(self):
        raise NotImplementedError
