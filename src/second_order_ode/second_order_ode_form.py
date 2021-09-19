from enum import Enum, auto
from tkinter import messagebox, Button, Entry
from typing import Dict

import src.second_order_ode.second_order_ode_messages as messages
import src.tkinter_config as config
from src.differential_equation_form import DifferentialEquationForm
from src.differential_equation_metadata import SecondOrderODEMetadata
from src.equation_form_builder import EquationFormBuilder
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

    def __init__(self, frame, fig, canvas):
        DifferentialEquationForm.__init__(self, frame, fig, canvas)

    def initialize_widgets(self):
        builder: EquationFormBuilder[SecondOrderODEFields] = EquationFormBuilder[SecondOrderODEFields](self)
        builder.build_entry_row(SecondOrderODEFields.SOURCE,
                                messages.source_term,
                                messages.source_term_symbol, 0)
        builder.build_entry_row(SecondOrderODEFields.INITIAL_VALUE,
                                messages.initial_value,
                                messages.initial_value_symbol, 1)
        builder.build_entry_row(SecondOrderODEFields.INITIAL_DERIVATIVE,
                                messages.initial_derivative,
                                messages.initial_derivative_symbol, 2)
        builder.build_entry_row(SecondOrderODEFields.TIME,
                                messages.time_interval,
                                messages.time_interval_symbol, 3)
        builder.build_entry_row(SecondOrderODEFields.SAMPLES,
                                messages.samples,
                                messages.samples_symbol, 4)
        self.field_entry_map = builder.get_field_entry_map()
        Button(self, text="Solve", font=config.details_font, width=10, command=self.solve).grid(
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
