from enum import Enum, auto
from tkinter import messagebox, Button, Entry
from typing import Dict

from src.differential_equation_messages import DifferentialEquationMessages
from src.differential_equation_metadata import SecondOrderODEMetadata
from src.differential_equation_form import DifferentialEquationForm
from src.second_order_ode.second_order_ode import SecondOrderODE


class SecondOrderODEFields(Enum):
    SOURCE = auto()
    INITIAL_VALUE = auto()
    INITIAL_DERIVATIVE = auto()
    TIME = auto()
    SAMPLES = auto()


class SecondOrderODEForm(DifferentialEquationForm):
    current_equation: SecondOrderODE
    field_entry_map: Dict[SecondOrderODEFields, Entry]

    def __init__(self, main_view):
        DifferentialEquationForm.__init__(self, main_view)

    def initialize_widgets(self):
        self.field_entry_map[SecondOrderODEFields.SOURCE] = self.create_field_entry(
            DifferentialEquationMessages.source_term,
            DifferentialEquationMessages.second_order_source_term_symbol, 0
        )
        self.field_entry_map[SecondOrderODEFields.INITIAL_VALUE] = self.create_field_entry(
            DifferentialEquationMessages.initial_value,
            DifferentialEquationMessages.initial_value_symbol, 1
        )
        self.field_entry_map[SecondOrderODEFields.INITIAL_DERIVATIVE] = self.create_field_entry(
            DifferentialEquationMessages.initial_derivative,
            DifferentialEquationMessages.initial_derivative_symbol, 2
        )
        self.field_entry_map[SecondOrderODEFields.TIME] = self.create_field_entry(
            DifferentialEquationMessages.time_interval,
            DifferentialEquationMessages.time_interval_symbol, 3
        )
        self.field_entry_map[SecondOrderODEFields.SAMPLES] = self.create_field_entry(
            DifferentialEquationMessages.samples,
            DifferentialEquationMessages.samples_symbol, 4
        )
        Button(self, text="Solve", font=self.font, width=10, command=self.solve).grid(
            row=5, column=2, pady=10, sticky="w"
        )

    def extract_diff_eq(self):
        return SecondOrderODE(
            SecondOrderODEMetadata(
                self.field_entry_map.get(SecondOrderODEFields.SOURCE).get(),
                float(self.field_entry_map.get(SecondOrderODEFields.INITIAL_VALUE).get()),
                float(self.field_entry_map.get(SecondOrderODEFields.INITIAL_DERIVATIVE).get()),
                int(self.field_entry_map.get(SecondOrderODEFields.SAMPLES).get()),
                float(self.field_entry_map.get(SecondOrderODEFields.TIME).get())
            )
        )

    def solve(self):
        try:
            self.current_equation = self.extract_diff_eq()
            self.current_equation.compute_solution()
            self.current_equation.save_solution(f"{self.data_folder_path}/second_order_ode.xlsx")
            messagebox.showinfo("Differential Equation Solver", "Your solution has been recorded")
            self.fig.clf()
            self.current_equation.initialize_figure(self.fig)
            self.canvas.draw()
        except Exception as err:
            messagebox.showinfo("Differential Equation Solver", err)
