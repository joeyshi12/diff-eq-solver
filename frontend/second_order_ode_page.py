import tkinter as tk
from tkinter import messagebox
from backend.differential_equation import InvalidQuery
from backend.second_order_ode import SecondOrderODE
from frontend.page import Page


class SecondOrderODEPage(Page):
    diff_eq: SecondOrderODE
    solve_button: tk.Button
    display_button: tk.Button

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        param_ids = ["source", "initial_value", "initial_derivative", "time", "samples"]
        param_names = ["Source term", "Initial value", "Initial derivative", "Time interval", "Samples"]
        param_symbols = ["f(t, x, y=x')", "x(0)", "x'(0)", "T", "N"]
        self.entries = {param_ids[i]: tk.Entry(self, font=self.font) for i in range(len(param_ids))}
        for i in range(len(param_ids)):
            tk.Label(self, text=param_names[i] + ":", font=self.font,
                     background=self.bgcolor).grid(row=i, column=0, padx=18, pady=10, sticky="w")
            tk.Label(self, text=param_symbols[i] + " = ", font=self.font,
                     background=self.bgcolor).grid(row=i, column=1, padx=0, pady=10, sticky="e")
            self.entries[param_ids[i]].grid(row=i, column=2, pady=0)
        self.solve_button = tk.Button(self, text="Solve", font=self.font, width=10, command=self.solve)
        self.solve_button.grid(row=6, column=2, pady=10, sticky="w")
        tk.Button(self, text="Reset", font=self.font, width=10, command=self.reset).grid(row=8, column=2, sticky="w")

    def solve(self):
        try:
            query = {"samples": int(self.entries["samples"].get()),
                     "time": float(self.entries["time"].get()),
                     "initial_value": float(self.entries["initial_value"].get()),
                     "initial_derivative": float(self.entries["initial_derivative"].get()),
                     "source": self.entries["source"].get()}
            self.diff_eq = SecondOrderODE(query)
        except ValueError or InvalidQuery:
            messagebox.showinfo("Differential Equation Solver", "Invalid value encountered in one of the entries")
            return
        self.diff_eq.solve()
        self.diff_eq.record_solution("../outputs/second_order_ode.xlsx")
        messagebox.showinfo("Differential Equation Solver",
                            "Your solution has been written in outputs/second_order_ode")
        self.solve_button.destroy()
        self.display_button = tk.Button(self, text="Display", font=self.font, width=10, command=self.diff_eq.display)
        self.display_button.grid(row=5, column=2, pady=10, sticky="w")

    def reset(self):
        self.display_button.destroy()
        self.solve_button = tk.Button(self, text="Solve", font=self.font, width=10, command=self.solve)
        self.solve_button.grid(row=5, column=2, pady=10, sticky="w")
