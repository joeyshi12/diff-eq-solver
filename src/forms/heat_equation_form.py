from enum import Enum, auto
from tkinter import messagebox, StringVar, Button, Entry, Frame
from typing import Union

import src.messages.common_messages as common_messages
import src.messages.heat_equation_messages as messages
from src.differential_equation_metadata import BoundaryConditions, BoundaryCondition, HeatEquationMetadata, BoundaryType
from src.forms.differential_equation_form import DifferentialEquationForm
from src.forms.equation_form_builder import EquationFormBuilder
from src.services.heat_equation_service import HeatEquationService


class HeatEquationFields(Enum):
    LEFT_BOUNDARY_TYPE = auto()
    RIGHT_BOUNDARY_TYPE = auto()
    LEFT_BOUNDARY_VALUES = auto()
    RIGHT_BOUNDARY_VALUES = auto()
    INITIAL_VALUES = auto()
    SOURCE = auto()
    ALPHA = auto()
    LENGTH = auto()
    TIME = auto()
    SAMPLES = auto()


class HeatEquationForm(DifferentialEquationForm):
    equation_service: HeatEquationService
    field_entry_map: dict[HeatEquationFields, Union[Entry, StringVar]]
    solve_button: Button
    render_plot_button: Button
    toggle_animation_button: Button

    def __init__(self, frame: Frame, canvas, equation_service):
        DifferentialEquationForm.__init__(self, frame, canvas)
        self.equation_service = equation_service

    def build_form(self):
        builder = EquationFormBuilder[HeatEquationFields](self)
        self.build_entries(builder)
        self.build_buttons(builder)

    def build_entries(self, builder: EquationFormBuilder[HeatEquationFields]):
        builder.build_boundary_type_section(HeatEquationFields.LEFT_BOUNDARY_TYPE,
                                            HeatEquationFields.RIGHT_BOUNDARY_TYPE)
        builder.build_entry_row(HeatEquationFields.LEFT_BOUNDARY_VALUES,
                                messages.left_boundary_values,
                                messages.left_boundary_type_symbol, 2)
        builder.build_entry_row(HeatEquationFields.RIGHT_BOUNDARY_VALUES,
                                messages.right_boundary_values,
                                messages.right_boundary_type_symbol, 3)
        builder.build_entry_row(HeatEquationFields.INITIAL_VALUES,
                                messages.initial_values,
                                messages.initial_values_symbol, 4)
        builder.build_entry_row(HeatEquationFields.SOURCE,
                                messages.source_term,
                                messages.source_term_symbol, 5)
        builder.build_entry_row(HeatEquationFields.ALPHA,
                                messages.diffusivity,
                                messages.diffusivity_symbol, 6)
        builder.build_entry_row(HeatEquationFields.LENGTH,
                                messages.length,
                                messages.length_symbol, 7)
        builder.build_entry_row(HeatEquationFields.TIME,
                                messages.time_interval,
                                messages.time_interval_symbol, 8)
        builder.build_entry_row(HeatEquationFields.SAMPLES,
                                messages.samples,
                                messages.samples_symbol, 9)
        self.field_entry_map = builder.get_field_entry_map()

    def build_buttons(self, builder: EquationFormBuilder[HeatEquationFields]):
        self.solve_button = builder.create_button(common_messages.solve, callback=self.solve)
        self.render_plot_button = builder.create_button(common_messages.show_plot, callback=self.handle_render_plot)
        self.toggle_animation_button = builder.create_button(common_messages.play,
                                                             callback=self.handle_toggle_animation)
        self.solve_button.grid(row=10, column=2, pady=6, sticky="w")

    def get_equation_metadata(self):
        left_boundary_type = BoundaryType(self.field_entry_map[HeatEquationFields.LEFT_BOUNDARY_TYPE].get())
        right_boundary_type = BoundaryType(self.field_entry_map[HeatEquationFields.RIGHT_BOUNDARY_TYPE].get())
        boundary_conditions = BoundaryConditions(
            BoundaryCondition(left_boundary_type,
                              self.field_entry_map[HeatEquationFields.LEFT_BOUNDARY_VALUES].get()),
            BoundaryCondition(right_boundary_type,
                              self.field_entry_map[HeatEquationFields.RIGHT_BOUNDARY_VALUES].get()))
        source = self.field_entry_map[HeatEquationFields.SOURCE].get()
        return HeatEquationMetadata(
            boundary_conditions,
            float(self.field_entry_map[HeatEquationFields.LENGTH].get()),
            int(self.field_entry_map[HeatEquationFields.SAMPLES].get()),
            float(self.field_entry_map[HeatEquationFields.TIME].get()),
            float(self.field_entry_map[HeatEquationFields.ALPHA].get()),
            self.field_entry_map[HeatEquationFields.INITIAL_VALUES].get(),
            source if source else "0"
        )

    def solve(self):
        try:
            self.equation_service.compute_and_update_solution(self.get_equation_metadata())
            messagebox.showinfo(common_messages.app_name,
                                common_messages.solution_recorded_message.format(self.equation_service.table_path))
            self.render_plot_button.grid(row=10, column=3, pady=6, sticky="e")
            self.toggle_animation_button.grid(row=11, column=3, pady=6, sticky="e")
            self.canvas.draw()
        except Exception as err:
            messagebox.showinfo(common_messages.app_name, err)

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