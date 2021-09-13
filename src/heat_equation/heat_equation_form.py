from enum import Enum, auto
from tkinter import messagebox, StringVar, Label
from tkinter.ttk import Radiobutton, Button, Entry

from src.differential_equation_messages import DifferentialEquationMessages
from src.differential_equation_metadata import BoundaryConditions, BoundaryCondition, HeatEquationMetadata, BoundaryType
from src.differential_equation_form import DifferentialEquationForm
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
    current_equation: HeatEquation
    entries: dict
    solve_button: Button
    display_button: Button
    animate_button: Button
    play_button: Button
    pause_button: Button
    anim = None

    def __init__(self, main_view):
        DifferentialEquationForm.__init__(self, main_view)
        param_ids = ["left_type",
                     "right_type",
                     "left_values",
                     "right_values",
                     "initial_condition",
                     "source",
                     "alpha",
                     "length",
                     "time",
                     "samples"]
        param_names = ["Left boundary type",
                       "Right boundary type",
                       "Left boundary values",
                       "Right boundary values",
                       "Initial values",
                       "Source term (optional)",
                       "Diffusivity",
                       "Length",
                       "Time interval",
                       "Samples"]
        param_symbols = [None, None, "φ₁(t)", "φ₂(t)", "u(0, x)", "s(t, x)", "α", "L", "T", "N"]

    def initialize_widgets(self):
        self.initialize_boundary_type_widgets()
        self.initialize_entries()
        self.place_buttons()

    def initialize_entries(self):
        fields = [
            HeatEquationFields.LEFT_BOUNDARY_TYPE,
            HeatEquationFields.RIGHT_BOUNDARY_TYPE,
            HeatEquationFields.LEFT_BOUNDARY_VALUES,
            HeatEquationFields.RIGHT_BOUNDARY_VALUES,
            HeatEquationFields.INITIAL_CONDITION,
            HeatEquationFields.SOURCE,
            HeatEquationFields.ALPHA,
            HeatEquationFields.LENGTH,
            HeatEquationFields.TIME,
            HeatEquationFields.SAMPLES
        ]
        self.fieldEntryMap = {field: Entry(self, font=self.font) for field in fields}
        for i in range(len(fields)):
            Label(self, text=param_names[i] + ":", font=self.font, background=self.bgcolour).grid(
                row=i, column=0, padx=18, pady=6, sticky="w")
            Label(self, text=param_symbols[i] + " = ", font=self.font, background=self.bgcolour).grid(
                row=i, column=1, pady=6, sticky="e")
            self.entries[param_ids[i]].grid(row=i, column=2, columnspan=2)

    def initialize_boundary_type_widgets(self):
        self.fieldEntryMap[HeatEquationFields.LEFT_BOUNDARY_TYPE] = StringVar(value=BoundaryType.DIRICHLET)
        self.fieldEntryMap[HeatEquationFields.RIGHT_BOUNDARY_TYPE] = StringVar(value=BoundaryType.DIRICHLET)
        Radiobutton(
            self,
            text=DifferentialEquationMessages.dirichlet,
            font=self.font,
            background=self.bgcolour,
            activebackground=self.bgcolour,
            variable=self.fieldEntryMap.get(HeatEquationFields.LEFT_BOUNDARY_TYPE),
            value=BoundaryType.DIRICHLET).grid(row=0, column=1, sticky="w")
        Radiobutton(
            self,
            text=DifferentialEquationMessages.neumann,
            font=self.font,
            background=self.bgcolour,
            activebackground=self.bgcolour,
            variable=self.fieldEntryMap.get(HeatEquationFields.LEFT_BOUNDARY_TYPE),
            value=BoundaryType.NEUMANN).grid(row=0, column=2, sticky="w")
        Radiobutton(
            self,
            text=DifferentialEquationMessages.dirichlet,
            font=self.font,
            background=self.bgcolour,
            activebackground=self.bgcolour,
            variable=self.fieldEntryMap.get(HeatEquationFields.RIGHT_BOUNDARY_TYPE),
            value=BoundaryType.DIRICHLET).grid(row=1, column=1, sticky="w")
        Radiobutton(
            self,
            text=DifferentialEquationMessages.neumann,
            font=self.font,
            background=self.bgcolour,
            activebackground=self.bgcolour,
            variable=self.fieldEntryMap.get(HeatEquationFields.RIGHT_BOUNDARY_TYPE),
            value=BoundaryType.NEUMANN).grid(row=1, column=2, sticky="w")

    def place_buttons(self):
        self.solve_button = tk.Button(self, text="Solve", font=self.font, width=10, command=self.solve)
        self.solve_button.grid(row=10, column=2, pady=6, sticky="w")
        self.display_button = tk.Button(self, text="Display", font=self.font, width=10)
        self.animate_button = tk.Button(self, text="Animate", font=self.font, width=10)
        self.play_button = tk.Button(self, text="Play", font=self.font, width=10, command=self.play_animation)
        self.pause_button = tk.Button(self, text="Pause", font=self.font, width=10, command=self.pause_animation)

    def build_equation(self):
        boundary_conditions = BoundaryConditions(
            BoundaryCondition(self.entries["left_type"].get(), self.entries["left_values"].get()),
            BoundaryCondition(self.entries["right_type"].get(), self.entries["right_values"].get())
        )
        return HeatEquation(
            HeatEquationMetadata(
                boundary_conditions,
                float(self.entries["alpha"].get()),
                float(self.entries["length"].get()),
                float(self.entries["time"].get()),
                int(self.entries["samples"].get()),
                self.entries["initial_condition"].get(),
                self.entries["source"].get() if not self.entries["source"].get() else "0"
            )
        )

    def solve(self):
        try:
            self.current_equation = self.build_equation()
            self.current_equation.compute_solution()
            self.current_equation.save_solution(f"{self.data_folder_path}/heat_equation_1d.xlsx")
            messagebox.showinfo(DifferentialEquationMessages.title, "Your solution has been recorded")
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
        self.animate_button.grid(row=11, column=3, pady=6, sticky="e")
        self.current_equation.initialize_figure(self.fig)
        self.canvas.draw()
        self.play_button.grid_forget()
        self.pause_button.grid_forget()

    def get_animation(self):
        self.fig.clf()
        self.anim = self.current_equation.get_animation(self.fig)
        self.canvas.draw()
        self.pause_button.grid(row=11, column=3, pady=6, sticky="e")
        self.animate_button.grid_forget()

    def pause_animation(self):
        self.play_button.grid(row=11, column=3, pady=6, sticky="e")
        self.pause_button.grid_forget()
        self.anim.event_source.stop()

    def play_animation(self):
        self.pause_button.grid(row=11, column=3, pady=6, sticky="e")
        self.play_button.grid_forget()
        self.anim.event_source.start()

    def clear_form(self):
        if self.anim:
            self.pause_animation()
        if self.current_equation:
            self.play_button.grid_forget()
            self.animate_button.grid(row=11, column=3, pady=6, sticky="e")
            self.fig.clf()
            self.canvas.draw()
