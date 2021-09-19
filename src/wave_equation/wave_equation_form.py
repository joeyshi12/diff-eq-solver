from enum import auto, Enum
from tkinter import messagebox, Button, Entry, Variable
from typing import Union

import src.tkinter_config as config
import src.wave_equation.wave_equation_messages as messages
from src.differential_equation_form import DifferentialEquationForm
from src.differential_equation_metadata import BoundaryConditions, BoundaryCondition, WaveEquationMetadata
from src.equation_form_builder import EquationFormBuilder
from src.wave_equation.wave_equation import WaveEquation


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
    field_entry_map: dict[WaveEquationFields, Union[Entry, Variable]]
    diff_eq: WaveEquation = None
    solve_button: Button
    display_button: Button
    animate_button: Button
    play_button: Button
    pause_button: Button
    file_name: str = "wave_equation_1d.xlsx"
    anim = None

    def __init__(self, frame, fig, canvas):
        DifferentialEquationForm.__init__(self, frame, fig, canvas)

    def initialize_widgets(self):
        builder: EquationFormBuilder[WaveEquationFields] = EquationFormBuilder[WaveEquationFields](self)
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
        self.place_buttons()

    def place_buttons(self):
        self.solve_button = Button(self, text="Solve", font=config.details_font, width=10, command=self.solve)
        self.solve_button.grid(row=11, column=2, pady=6, sticky="w")
        self.display_button = Button(self, text="Display", font=config.details_font, width=10)
        self.animate_button = Button(self, text="Animate", font=config.details_font, width=10)
        self.play_button = Button(self, text="Play", font=config.details_font, width=10, command=self.play_animation)
        self.pause_button = Button(self, text="Pause", font=config.details_font, width=10, command=self.pause_animation)

    def extract_diff_eq(self):
        boundary_conditions = BoundaryConditions(
            BoundaryCondition(self.field_entry_map[WaveEquationFields.LEFT_BOUNDARY_TYPE].get(),
                              self.field_entry_map[WaveEquationFields.LEFT_BOUNDARY_VALUES].get()),
            BoundaryCondition(self.field_entry_map[WaveEquationFields.RIGHT_BOUNDARY_TYPE].get(),
                              self.field_entry_map[WaveEquationFields.RIGHT_BOUNDARY_VALUES].get())
        )
        source = self.field_entry_map[WaveEquationFields.SOURCE].get()
        return WaveEquation(
            WaveEquationMetadata(
                boundary_conditions,
                eval(self.field_entry_map[WaveEquationFields.WAVE_SPEED].get()),
                eval(self.field_entry_map[WaveEquationFields.LENGTH].get()),
                eval(self.field_entry_map[WaveEquationFields.TIME].get()),
                int(self.field_entry_map[WaveEquationFields.SAMPLES].get()),
                self.field_entry_map[WaveEquationFields.INITIAL_VALUES].get(),
                self.field_entry_map[WaveEquationFields.INITIAL_DERIVATIVES].get(),
                source if source else "0"
            )
        )

    def solve(self):
        try:
            self.diff_eq = self.extract_diff_eq()
            self.diff_eq.compute_solution()
            self.diff_eq.save_solution("outputs/" + self.file_name)
        except Exception as err:
            messagebox.showinfo("Differential Equation Solver", err)
            return
        messagebox.showinfo("Differential Equation Solver", "Your solution has been recorded")
        self.display_button.configure(command=self.display)
        self.display_button.grid(row=11, column=3, pady=6, sticky="e")
        self.animate_button.configure(command=self.get_animation)
        self.animate_button.grid(row=12, column=3, pady=6, sticky="e")
        self.display()

    def display(self):
        if self.anim:
            self.pause_animation()
        self.fig.clf()
        self.animate_button.configure(command=self.get_animation)
        self.animate_button.grid(row=12, column=3, pady=6, sticky="e")
        self.diff_eq.initialize_figure(self.fig)
        self.canvas.draw()
        self.play_button.grid_forget()
        self.pause_button.grid_forget()

    def get_animation(self):
        self.fig.clf()
        self.anim = self.diff_eq.get_animation(self.fig)
        self.canvas.draw()
        self.pause_button.grid(row=12, column=3, pady=6, sticky="e")
        self.animate_button.grid_forget()

    def pause_animation(self):
        self.play_button.grid(row=12, column=3, pady=6, sticky="e")
        self.pause_button.grid_forget()
        self.anim.event_source.stop()

    def play_animation(self):
        self.pause_button.grid(row=12, column=3, pady=6, sticky="e")
        self.play_button.grid_forget()
        self.anim.event_source.start()

    def reset(self):
        if self.anim:
            self.pause_animation()
            self.anim = None
        if self.diff_eq:
            self.play_button.grid_forget()
            self.animate_button.grid(row=12, column=3, pady=6, sticky="e")
            self.fig.clf()
            self.canvas.draw()
