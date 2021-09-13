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
    field_entry_map: Dict[FirstOrderODEFields, Entry]

    def __init__(self, main_view):
        DifferentialEquationForm.__init__(self, main_view)

    def initialize_widgets(self):
        self.field_entry_map[FirstOrderODEFields.SOURCE] = self.create_field_entry(
            DifferentialEquationMessages.source_term,
            DifferentialEquationMessages.source_term_symbol, 0
        )
        self.field_entry_map[FirstOrderODEFields.INITIAL_VALUE] = self.create_field_entry(
            DifferentialEquationMessages.initial_value,
            DifferentialEquationMessages.initial_value_symbol, 1
        )
        self.field_entry_map[FirstOrderODEFields.TIME] = self.create_field_entry(
            DifferentialEquationMessages.time_interval,
            DifferentialEquationMessages.time_interval_symbol, 2
        )
        self.field_entry_map[FirstOrderODEFields.SAMPLES] = self.create_field_entry(
            DifferentialEquationMessages.samples,
            DifferentialEquationMessages.samples_symbol, 3
        )
        Button(self, text="Solve", font=self.font, width=10, command=self.solve).grid(
            row=5, column=2, pady=10, sticky="w")

    def build_equation(self):
        return FirstOrderODE(
            FirstOrderODEMetadata(
                self.field_entry_map.get(FirstOrderODEFields.SOURCE).get(),
                float(self.field_entry_map.get(FirstOrderODEFields.INITIAL_VALUE).get()),
                int(self.field_entry_map.get(FirstOrderODEFields.SAMPLES).get()),
                float(self.field_entry_map.get(FirstOrderODEFields.TIME).get())
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
