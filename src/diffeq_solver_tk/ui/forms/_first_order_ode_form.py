import tkinter as tk

from diffeq_solver_tk.diffeq import OrdinaryDifferentialEquationMetadata, OrdinaryDifferentialEquationService
from diffeq_solver_tk.ui.messages import common_messages, first_order_ode_messages as messages
from diffeq_solver_tk.ui.forms import DifferentialEquationForm


class FirstOrderODEForm(DifferentialEquationForm):
    def __init__(self, master: tk.Frame, canvas, equation_service: OrdinaryDifferentialEquationService):
        DifferentialEquationForm.__init__(self, master, canvas, equation_service)
        self.source_entry = tk.Entry(master=self, width=24)
        self.initial_value_entry = tk.Entry(master=self, width=24)
        self.time_entry = tk.Entry(master=self, width=24)
        self.samples_entry = tk.Entry(master=self, width=24)

        fields: list[tuple[str, str, tk.Entry]] = [
            (messages.source_term, messages.source_term_symbol, self.source_entry),
            (messages.initial_value, messages.initial_value_symbol, self.initial_value_entry),
            (messages.time_interval, messages.time_interval_symbol, self.time_entry),
            (messages.samples, messages.samples_symbol, self.samples_entry)
        ]
        for i, (label_text, symbol, input_entry) in enumerate(fields):
            tk.Label(master=self, text=label_text + ":").grid(row=i, column=0, pady=6, sticky="w")
            tk.Label(master=self, text=symbol + " = ").grid(row=i, column=1, pady=0, sticky="e")
            input_entry.grid(row=i, column=2, columnspan=2)

        tk.Button(master=self, text=common_messages.solve, width=10, command=self.solve_equation).grid(row=4, column=2, pady=10, sticky="w")
        self.export_button = tk.Button(master=self, text=common_messages.export, width=10, command=self.export_solution)

    def get_equation_metadata(self):
        return OrdinaryDifferentialEquationMetadata(
            self.source_entry.get(),
            [float(self.initial_value_entry.get())],
            int(self.samples_entry.get()),
            float(self.time_entry.get())
        )

    def on_solve(self):
        self.export_button.grid(row=5, column=2, sticky="w")
        self.canvas.draw()

    def reset(self):
        self.equation_service.clear_solution()
        self.export_button.grid_forget()
        self.canvas.draw()
