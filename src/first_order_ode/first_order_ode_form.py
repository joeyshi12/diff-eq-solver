from enum import Enum, auto
from tkinter import messagebox, Label, Entry, Button
from typing import Dict

from src.differential_equation_messages import DifferentialEquationMessages
from src.differential_equation_metadata import FirstOrderODEMetadata
from src.first_order_ode.first_order_ode import FirstOrderODE
from src.differential_equation_form import DifferentialEquationForm


class FirstOrderODEFields(Enum):
    SOURCE = auto()
    INITIAL_VALUE = auto()
    TIME = auto()
    SAMPLES = auto()


class FirstOrderODEForm(DifferentialEquationForm):
    current_equation: FirstOrderODE
    fieldEntryMap: Dict[FirstOrderODEFields, Entry]

    def __init__(self, main_view):
        DifferentialEquationForm.__init__(self, main_view)

    def initialize_widgets(self):
        fields = [
            FirstOrderODEFields.SOURCE,
            FirstOrderODEFields.INITIAL_VALUE,
            FirstOrderODEFields.TIME,
            FirstOrderODEFields.SAMPLES
        ]
        display_names = [
            DifferentialEquationMessages.source_term,
            DifferentialEquationMessages.initial_value,
            DifferentialEquationMessages.time_interval,
            DifferentialEquationMessages.samples
        ]
        symbol_names = [
            DifferentialEquationMessages.source_term_symbol,
            DifferentialEquationMessages.initial_value_symbol,
            DifferentialEquationMessages.time_interval_symbol,
            DifferentialEquationMessages.samples_symbol
        ]
        self.fieldEntryMap = {field: Entry(self, font=self.font) for field in fields}
        for i in range(len(fields)):
            Label(self, text=f"{display_names[i]}:", font=self.font, background=self.bgcolour).grid(
                row=i, column=0, padx=18, pady=10, sticky="w")
            Label(self, text=f"{symbol_names[i]} = ", font=self.font, background=self.bgcolour).grid(
                row=i, column=1, padx=0, pady=10, sticky="e")
            self.fieldEntryMap.get(fields[i]).grid(row=i, column=2, pady=0)
        Button(self, text="Solve", font=self.font, width=10, command=self.solve).grid(
            row=5, column=2, pady=10, sticky="w")

    def clear_form(self):
        pass

    def build_equation(self):
        return FirstOrderODE(
            FirstOrderODEMetadata(
                self.fieldEntryMap.get(FirstOrderODEFields.SOURCE).get(),
                float(self.fieldEntryMap.get(FirstOrderODEFields.INITIAL_VALUE).get()),
                int(self.fieldEntryMap.get(FirstOrderODEFields.SAMPLES).get()),
                float(self.fieldEntryMap.get(FirstOrderODEFields.TIME).get())
            )
        )

    async def solve(self):
        try:
            self.current_equation = self.build_equation()
            self.current_equation.compute_solution()
            self.current_equation.save_solution(f"${self.data_folder_path}/first_order_ode.xlsx")
            messagebox.showinfo("Differential Equation Solver", "Your solution has been recorded")
            self.fig.clf()
            self.current_equation.initialize_figure(self.fig)
            self.canvas.draw()
        except Exception as err:
            messagebox.showinfo("Differential Equation Solver", err)
