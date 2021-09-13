from enum import Enum, auto
from tkinter import messagebox, Button, Label, Entry

from src.differential_equation_messages import DifferentialEquationMessages
from src.differential_equation_metadata import SecondOrderODEMetadata
from src.differential_equation_form import DifferentialEquationForm
from src.second_order_ode.second_order_ode import SecondOrderODE


class SecondOrderODEFields(Enum):
    SOURCE = auto()
    INITIAL_VALUE = auto()
    INITIAL_DERIVATIVE = auto()
    TIME = auto()
    SAMPLES = auto()


class SecondOrderODEForm(DifferentialEquationForm):
    current_equation: SecondOrderODE
    fieldEntryMap: dict
    file_name: str = "second_order_ode.xlsx"

    def __init__(self, main_view):
        DifferentialEquationForm.__init__(self, main_view)

    def initialize_widgets(self):
        fields = [
            SecondOrderODEFields.SOURCE,
            SecondOrderODEFields.INITIAL_VALUE,
            SecondOrderODEFields.INITIAL_DERIVATIVE,
            SecondOrderODEFields.TIME,
            SecondOrderODEFields.SAMPLES
        ]
        display_names = [
            DifferentialEquationMessages.source_term,
            DifferentialEquationMessages.initial_value,
            DifferentialEquationMessages.initial_derivative,
            DifferentialEquationMessages.time_interval,
            DifferentialEquationMessages.samples
        ]
        symbol_names = [
            DifferentialEquationMessages.second_order_source_term_symbol,
            DifferentialEquationMessages.initial_value_symbol,
            DifferentialEquationMessages.initial_derivative_symbol,
            DifferentialEquationMessages.time_interval_symbol,
            DifferentialEquationMessages.samples_symbol
        ]
        self.fieldEntryMap = {field: Entry(self, font=self.font) for field in fields}
        for i in range(len(fields)):
            Label(self, text=f"{display_names[i]}:", font=self.font, background=self.bgcolour).grid(
                row=i, column=0, padx=18, pady=10, sticky="w")
            Label(self, text=f"{symbol_names[i]} = ", font=self.font, background=self.bgcolour).grid(
                row=i, column=1, padx=0, pady=10, sticky="e")
            self.fieldEntryMap.get(fields[i]).grid(row=i, column=2, pady=0)
        Button(self, text="Solve", font=self.font, width=10, command=self.solve).grid(
            row=6, column=2, pady=10, sticky="w")

    def clear_form(self):
        pass

    def extract_diff_eq(self):
        return SecondOrderODE(
            SecondOrderODEMetadata(
                self.fieldEntryMap["source"].get(),
                float(self.fieldEntryMap["initial_value"].get()),
                float(self.fieldEntryMap["initial_derivative"].get()),
                int(self.fieldEntryMap["samples"].get()),
                float(self.fieldEntryMap["time"].get())
            )
        )

    def solve(self):
        try:
            self.current_equation = self.extract_diff_eq()
            self.current_equation.compute_solution()
            self.current_equation.save_solution("outputs/" + self.file_name)
            messagebox.showinfo("Differential Equation Solver", "Your solution has been recorded")
            self.fig.clf()
            self.current_equation.initialize_figure(self.fig)
            self.canvas.draw()
        except Exception as err:
            messagebox.showinfo("Differential Equation Solver", err)
