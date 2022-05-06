from enum import Enum, auto
from tkinter import Entry, Frame, Button
from typing import Dict

import diffeq_solver_tk.messages.common_messages as common_messages
import diffeq_solver_tk.messages.second_order_ode_messages as messages
from diffeq_solver_tk.differential_equation_metadata import OrdinaryDifferentialEquationMetadata
from diffeq_solver_tk.forms.differential_equation_form import DifferentialEquationForm
from diffeq_solver_tk.forms.equation_form_builder import EquationFormBuilder
from diffeq_solver_tk.services.second_order_ode_service import SecondOrderODEService


class SecondOrderODEFields(Enum):
    SOURCE = auto()
    INITIAL_VALUE = auto()
    INITIAL_DERIVATIVE = auto()
    TIME = auto()
    SAMPLES = auto()


class SecondOrderODEForm(DifferentialEquationForm):
    equation_service: SecondOrderODEService
    field_entry_map: Dict[SecondOrderODEFields, Entry]
    export_button: Button

    def __init__(self, frame: Frame, canvas, equation_service: SecondOrderODEService):
        DifferentialEquationForm.__init__(self, frame, canvas, equation_service)

    def build_form(self):
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
        builder.create_button(common_messages.solve,
                              callback=self.solve_equation).grid(row=5, column=2, pady=10, sticky="w")
        self.export_button = builder.create_button(common_messages.export, callback=self.export_solution)

    def get_equation_metadata(self):
        initial_derivatives = [
            float(self.field_entry_map.get(SecondOrderODEFields.INITIAL_VALUE).get()),
            float(self.field_entry_map.get(SecondOrderODEFields.INITIAL_DERIVATIVE).get())
        ]
        return OrdinaryDifferentialEquationMetadata(
            self.field_entry_map.get(SecondOrderODEFields.SOURCE).get(),
            initial_derivatives,
            int(self.field_entry_map.get(SecondOrderODEFields.SAMPLES).get()),
            float(self.field_entry_map.get(SecondOrderODEFields.TIME).get())
        )

    def on_solve(self):
        self.export_button.grid(row=6, column=2, sticky="w")

    def reset(self):
        self.equation_service.clear_solution()
        self.export_button.grid_forget()
        self.canvas.draw()
