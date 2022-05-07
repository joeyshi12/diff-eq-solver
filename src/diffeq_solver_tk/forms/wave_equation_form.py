from enum import auto, Enum
from tkinter import Button, Entry, Variable, Frame
from typing import Union, Dict

import diffeq_solver_tk.messages.common_messages as common_messages
import diffeq_solver_tk.messages.wave_equation_messages as messages
from diffeq_solver_tk.differential_equation_metadata import BoundaryConditions, BoundaryCondition, WaveEquationMetadata, BoundaryType
from diffeq_solver_tk.forms.differential_equation_form import DifferentialEquationForm
from diffeq_solver_tk.forms.equation_form_builder import EquationFormBuilder
from diffeq_solver_tk.services.wave_equation_service import WaveEquationService


class WaveEquationFields(Enum):
    LEFT_BOUNDARY_TYPE = auto()
    RIGHT_BOUNDARY_TYPE = auto()
    LEFT_BOUNDARY_VALUES = auto()
    RIGHT_BOUNDARY_VALUES = auto()
    INITIAL_VALUES = auto()
    INITIAL_DERIVATIVES = auto()
    SOURCE = auto()
    WAVE_SPEED = auto()
    ALPHA = auto()
    LENGTH = auto()
    TIME = auto()
    SAMPLES = auto()


class WaveEquationForm(DifferentialEquationForm):
    field_entry_map: Dict[WaveEquationFields, Union[Entry, Variable]]
    equation_service: WaveEquationService
    solve_button: Button
    export_button: Button
    render_plot_button: Button
    toggle_animation_button: Button

    def __init__(self, frame: Frame, canvas, equation_service: WaveEquationService):
        DifferentialEquationForm.__init__(self, frame, canvas, equation_service)

    def build_form(self):
        builder = EquationFormBuilder[WaveEquationFields](self)
        self.build_entries(builder)
        self.build_buttons(builder)

    def build_entries(self, builder: EquationFormBuilder[WaveEquationFields]):
        builder.build_boundary_type_section(WaveEquationFields.LEFT_BOUNDARY_TYPE,
                                            WaveEquationFields.RIGHT_BOUNDARY_TYPE)
        builder.build_entry_row(WaveEquationFields.LEFT_BOUNDARY_VALUES,
                                messages.left_boundary_values,
                                messages.left_boundary_values_symbol, 2)
        builder.build_entry_row(WaveEquationFields.RIGHT_BOUNDARY_VALUES,
                                messages.right_boundary_values,
                                messages.right_boundary_values_symbol, 3)
        builder.build_entry_row(WaveEquationFields.INITIAL_VALUES,
                                messages.initial_values,
                                messages.initial_values_symbol, 4)
        builder.build_entry_row(WaveEquationFields.INITIAL_DERIVATIVES,
                                messages.initial_derivatives,
                                messages.initial_derivatives_symbol, 5)
        builder.build_entry_row(WaveEquationFields.SOURCE,
                                messages.source_term,
                                messages.source_term_symbol, 6)
        builder.build_entry_row(WaveEquationFields.WAVE_SPEED,
                                messages.wave_speed,
                                messages.wave_speed_symbol, 7)
        builder.build_entry_row(WaveEquationFields.LENGTH,
                                messages.length,
                                messages.length_symbol, 8)
        builder.build_entry_row(WaveEquationFields.TIME,
                                messages.time_interval,
                                messages.time_interval_symbol, 9)
        builder.build_entry_row(WaveEquationFields.SAMPLES,
                                messages.samples,
                                messages.samples_symbol, 10)
        self.field_entry_map = builder.get_field_entry_map()

    def build_buttons(self, builder: EquationFormBuilder[WaveEquationFields]):
        self.solve_button = builder.create_button(common_messages.solve, callback=self.solve_equation)
        self.export_button = builder.create_button(common_messages.export, callback=self.export_solution)
        self.render_plot_button = builder.create_button(common_messages.show_plot, callback=self.handle_render_plot)
        self.toggle_animation_button = builder.create_button(common_messages.play,
                                                             callback=self.handle_toggle_animation)
        self.solve_button.grid(row=11, column=2, pady=6, sticky="w")

    def get_equation_metadata(self):
        left_boundary_type = BoundaryType(self.field_entry_map[WaveEquationFields.LEFT_BOUNDARY_TYPE].get())
        right_boundary_type = BoundaryType(self.field_entry_map[WaveEquationFields.RIGHT_BOUNDARY_TYPE].get())
        boundary_conditions = BoundaryConditions(
            BoundaryCondition(left_boundary_type,
                              self.field_entry_map[WaveEquationFields.LEFT_BOUNDARY_VALUES].get()),
            BoundaryCondition(right_boundary_type,
                              self.field_entry_map[WaveEquationFields.RIGHT_BOUNDARY_VALUES].get()))
        source = self.field_entry_map[WaveEquationFields.SOURCE].get()
        return WaveEquationMetadata(
            boundary_conditions,
            float(self.field_entry_map[WaveEquationFields.LENGTH].get()),
            int(self.field_entry_map[WaveEquationFields.SAMPLES].get()),
            float(self.field_entry_map[WaveEquationFields.TIME].get()),
            float(self.field_entry_map[WaveEquationFields.WAVE_SPEED].get()),
            self.field_entry_map[WaveEquationFields.INITIAL_VALUES].get(),
            self.field_entry_map[WaveEquationFields.INITIAL_DERIVATIVES].get(),
            source if source else "0"
        )

    def on_solve(self):
        self.render_plot_button.grid(row=11, column=3, pady=6, sticky="e")
        self.toggle_animation_button.grid(row=12, column=3, pady=6, sticky="e")
        self.export_button.grid(row=13, column=3, pady=6, sticky="e")

    def handle_render_plot(self):
        self.toggle_animation_button.configure(text=common_messages.play)
        self.equation_service.render_current_solution()
        self.canvas.draw()

    def handle_toggle_animation(self):
        self.equation_service.toggle_animation()
        self.canvas.draw()
        if self.equation_service.is_animation_playing():
            self.toggle_animation_button.configure(text=common_messages.pause)
        else:
            self.toggle_animation_button.configure(text=common_messages.play)

    def reset(self):
        self.equation_service.clear_solution()
        self.equation_service.clear_animation()
        self.canvas.draw()
        self.render_plot_button.grid_forget()
        self.toggle_animation_button.grid_forget()
        self.export_button.grid_forget()
