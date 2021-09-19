from enum import Enum, auto
from tkinter import messagebox, Entry, Button
from typing import Dict

import src.first_order_ode.first_order_ode_messages as messages
import src.tkinter_config as config
from src.differential_equation_form import DifferentialEquationForm
from src.differential_equation_metadata import FirstOrderODEMetadata
from src.equation_form_builder import EquationFormBuilder
from src.first_order_ode.first_order_ode import FirstOrderODE


class FirstOrderODEFields(Enum):
    SOURCE = auto()
    INITIAL_VALUE = auto()
    TIME = auto()
    SAMPLES = auto()


class FirstOrderODEForm(DifferentialEquationForm):
    current_equation: FirstOrderODE
    field_entry_map: Dict[FirstOrderODEFields, Entry]

    def __init__(self, frame, fig, canvas):
        DifferentialEquationForm.__init__(self, frame, fig, canvas)

    def initialize_widgets(self):
        builder: EquationFormBuilder[FirstOrderODEFields] = EquationFormBuilder[FirstOrderODEFields](self)
        builder.build_entry_row(FirstOrderODEFields.SOURCE,
                                messages.source_term,
                                messages.source_term_symbol, 0)
        builder.build_entry_row(FirstOrderODEFields.INITIAL_VALUE,
                                messages.initial_value,
                                messages.initial_value_symbol, 1)
        builder.build_entry_row(FirstOrderODEFields.TIME,
                                messages.time_interval,
                                messages.time_interval_symbol, 2)
        builder.build_entry_row(FirstOrderODEFields.SAMPLES,
                                messages.samples,
                                messages.samples_symbol, 3)
        self.field_entry_map = builder.get_field_entry_map()
        Button(self, text="Solve", font=config.details_font, width=10, command=self.solve).grid(
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

    def solve(self):
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
