from enum import Enum, auto
from tkinter import messagebox, Entry, Frame, Button
from typing import Dict

import src.messages.common_messages as common_messages
import src.messages.first_order_ode_messages as messages
from src.differential_equation_metadata import OrdinaryDifferentialEquationMetadata
from src.forms.differential_equation_form import DifferentialEquationForm
from src.forms.equation_form_builder import EquationFormBuilder
from src.services.first_order_ode_service import FirstOrderODEService


class FirstOrderODEFields(Enum):
    SOURCE = auto()
    INITIAL_VALUE = auto()
    TIME = auto()
    SAMPLES = auto()


class FirstOrderODEForm(DifferentialEquationForm):
    equation_service: FirstOrderODEService
    field_entry_map: Dict[FirstOrderODEFields, Entry]

    def __init__(self, frame: Frame, canvas, equation_service: FirstOrderODEService):
        DifferentialEquationForm.__init__(self, frame, canvas)
        self.equation_service = equation_service

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
        button: Button = builder.create_button(common_messages.solve, callback=self.solve)
        button.grid(row=5, column=2, pady=10, sticky="w")

    def get_equation_metadata(self):
        return OrdinaryDifferentialEquationMetadata(
            self.field_entry_map.get(FirstOrderODEFields.SOURCE).get(),
            [float(self.field_entry_map.get(FirstOrderODEFields.INITIAL_VALUE).get())],
            int(self.field_entry_map.get(FirstOrderODEFields.SAMPLES).get()),
            float(self.field_entry_map.get(FirstOrderODEFields.TIME).get())
        )

    def solve(self):
        try:
            metadata = self.get_equation_metadata()
            self.equation_service.compute_and_update_solution(metadata)
            messagebox.showinfo(common_messages.app_name,
                                common_messages.solution_recorded_message.format(self.equation_service.table_path))
            self.canvas.draw()
        except Exception as err:
            messagebox.showinfo(common_messages.app_name, err)

    def reset(self):
        self.equation_service.clear_figure()
