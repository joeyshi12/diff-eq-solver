from enum import Enum, auto
from tkinter import messagebox, StringVar, Button, Entry
from typing import Union

import src.heat_equation.heat_equation_messages as messages
from src.differential_equation_form import DifferentialEquationForm
from src.differential_equation_metadata import BoundaryConditions, BoundaryCondition, HeatEquationMetadata, BoundaryType
from src.equation_form_builder import EquationFormBuilder
from src.heat_equation.heat_equation import HeatEquation


class HeatEquationFields(Enum):
    LEFT_BOUNDARY_TYPE = auto()
    RIGHT_BOUNDARY_TYPE = auto()
    LEFT_BOUNDARY_VALUES = auto()
    RIGHT_BOUNDARY_VALUES = auto()
    INITIAL_CONDITION = auto()
    SOURCE = auto()
    ALPHA = auto()
    LENGTH = auto()
    TIME = auto()
    SAMPLES = auto()


class HeatEquationForm(DifferentialEquationForm):
    equation: HeatEquation
    field_entry_map: dict[HeatEquationFields, Union[Entry, StringVar]]
    solve_button: Button
    display_button: Button
    animate_button: Button
    play_button: Button
    pause_button: Button
    anim = None

    def __init__(self, frame, fig, canvas):
        DifferentialEquationForm.__init__(self, frame, fig, canvas)

    def build_form(self):
        builder: EquationFormBuilder[HeatEquationFields] = EquationFormBuilder[HeatEquationFields](self)
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
        builder.build_entry_row(HeatEquationFields.INITIAL_CONDITION,
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
        self.solve_button = builder.create_button("Solve", callback=self.solve)
        self.display_button = builder.create_button("Display")
        self.animate_button = builder.create_button("Animate")
        self.play_button = builder.create_button("Play", callback=self.play_animation)
        self.pause_button = builder.create_button("Pause", callback=self.pause_animation)
        self.solve_button.grid(row=10, column=2, pady=6, sticky="w")

    def get_equation(self):
        left_boundary_type = BoundaryType(self.field_entry_map[HeatEquationFields.LEFT_BOUNDARY_TYPE].get())
        right_boundary_type = BoundaryType(self.field_entry_map[HeatEquationFields.RIGHT_BOUNDARY_TYPE].get())
        boundary_conditions = BoundaryConditions(
            BoundaryCondition(left_boundary_type,
                              self.field_entry_map[HeatEquationFields.LEFT_BOUNDARY_VALUES].get()),
            BoundaryCondition(right_boundary_type,
                              self.field_entry_map[HeatEquationFields.RIGHT_BOUNDARY_VALUES].get()))
        source = self.field_entry_map[HeatEquationFields.SOURCE].get()
        return HeatEquation(
            HeatEquationMetadata(
                boundary_conditions,
                float(self.field_entry_map[HeatEquationFields.ALPHA].get()),
                float(self.field_entry_map[HeatEquationFields.LENGTH].get()),
                float(self.field_entry_map[HeatEquationFields.TIME].get()),
                int(self.field_entry_map[HeatEquationFields.SAMPLES].get()),
                self.field_entry_map[HeatEquationFields.INITIAL_CONDITION].get(),
                source if source else "0"
            )
        )

    def solve(self):
        try:
            self.equation = self.get_equation()
            self.equation.compute_solution()
            self.equation.save_solution(f"{self.data_folder_path}/heat_equation_1d.xlsx")
            messagebox.showinfo("Error", "Your solution has been recorded")
            self.display_button.configure(command=self.display)
            self.display_button.grid(row=10, column=3, pady=6, sticky="e")
            self.animate_button.configure(command=self.get_animation)
            self.animate_button.grid(row=11, column=3, pady=6, sticky="e")
            self.display()
        except Exception as err:
            messagebox.showinfo("Differential Equation Solver", err)

    def display(self):
        if self.anim:
            self.pause_animation()
        self.fig.clf()
        self.animate_button.configure(command=self.get_animation)
        self.animate_button.grid(row=11, column=2, pady=6, sticky="e")
        self.equation.initialize_figure(self.fig)
        self.canvas.draw()
        self.play_button.grid_forget()
        self.pause_button.grid_forget()

    def get_animation(self):
        self.fig.clf()
        self.anim = self.equation.get_animation(self.fig)
        self.canvas.draw()
        self.pause_button.grid(row=11, column=2, pady=6, sticky="e")
        self.animate_button.grid_forget()

    def pause_animation(self):
        self.play_button.grid(row=11, column=2, pady=6, sticky="e")
        self.pause_button.grid_forget()
        self.anim.event_source.stop()

    def play_animation(self):
        self.pause_button.grid(row=11, column=2, pady=6, sticky="e")
        self.play_button.grid_forget()
        self.anim.event_source.start()

    def clear_form(self):
        if self.anim:
            self.pause_animation()
        if self.equation:
            self.play_button.grid_forget()
            self.animate_button.grid(row=11, column=2, pady=6, sticky="e")
            self.fig.clf()
            self.canvas.draw()
