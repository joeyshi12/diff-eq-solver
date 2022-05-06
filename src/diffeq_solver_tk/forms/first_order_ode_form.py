from enum import Enum, auto
from tkinter import Entry, Frame, Button
from typing import Dict

import diffeq_solver_tk.messages.common_messages as common_messages
import diffeq_solver_tk.messages.first_order_ode_messages as messages
from diffeq_solver_tk.differential_equation_metadata import OrdinaryDifferentialEquationMetadata
from diffeq_solver_tk.forms.differential_equation_form import DifferentialEquationForm
from diffeq_solver_tk.forms.equation_form_builder import EquationFormBuilder
from diffeq_solver_tk.services.first_order_ode_service import FirstOrderODEService


class FirstOrderODEFields(Enum):
    SOURCE = auto()
    INITIAL_VALUE = auto()
    TIME = auto()
    SAMPLES = auto()


class FirstOrderODEForm(DifferentialEquationForm):
    equation_service: FirstOrderODEService
    field_entry_map: Dict[FirstOrderODEFields, Entry]
    export_button: Button

    def __init__(self, frame: Frame, canvas, equation_service: FirstOrderODEService):
        DifferentialEquationForm.__init__(self, frame, canvas, equation_service)

    def build_form(self):
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
        builder.create_button(common_messages.solve,
                              callback=self.solve_equation).grid(row=5, column=2, pady=10, sticky="w")
        self.export_button = builder.create_button(common_messages.export, callback=self.export_solution)

    def get_equation_metadata(self):
        return OrdinaryDifferentialEquationMetadata(
            self.field_entry_map.get(FirstOrderODEFields.SOURCE).get(),
            [float(self.field_entry_map.get(FirstOrderODEFields.INITIAL_VALUE).get())],
            int(self.field_entry_map.get(FirstOrderODEFields.SAMPLES).get()),
            float(self.field_entry_map.get(FirstOrderODEFields.TIME).get())
        )

    def on_solve(self):
        self.export_button.grid(row=6, column=2, sticky="w")

    def reset(self):
        self.equation_service.clear_solution()
        self.export_button.grid_forget()
        self.canvas.draw()
