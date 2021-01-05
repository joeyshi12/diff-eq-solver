import tkinter as tk
from tkinter import messagebox
from backend.second_order_ode import SecondOrderODE
from frontend.page import Page


class SecondOrderODEPage(Page):
    diff_eq: SecondOrderODE
    entries: dict
    file_name: str = "second_order_ode.xlsx"

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        param_ids = ["source", "initial_value", "initial_derivative", "time", "samples"]
        param_names = ["Source term", "Initial value", "Initial derivative", "Time interval", "Samples"]
        param_symbols = ["f(t, x, y=x')", "x(0)", "x'(0)", "T", "N"]
        self.place_labels_and_entries(param_ids, param_names, param_symbols)
        tk.Button(self, text="Solve", font=self.font, width=10, command=self.solve).grid(row=6, column=2, pady=10,
                                                                                         sticky="w")

    def place_labels_and_entries(self, param_ids, param_names, param_symbols):
        self.entries = {param_ids[i]: tk.Entry(self, font=self.font) for i in range(len(param_ids))}
        for i in range(len(param_ids)):
            tk.Label(self, text=param_names[i] + ":", font=self.font,
                     background=self.bgcolour).grid(row=i, column=0, padx=18, pady=10, sticky="w")
            tk.Label(self, text=param_symbols[i] + " = ", font=self.font,
                     background=self.bgcolour).grid(row=i, column=1, padx=0, pady=10, sticky="e")
            self.entries[param_ids[i]].grid(row=i, column=2, pady=0)

    def extract_diff_eq(self):
        query = {"samples": int(self.entries["samples"].get()),
                 "time": float(self.entries["time"].get()),
                 "initial_value": float(self.entries["initial_value"].get()),
                 "initial_derivative": float(self.entries["initial_derivative"].get()),
                 "source": self.entries["source"].get()}
        return SecondOrderODE(query)

    def solve(self):
        try:
            self.diff_eq = self.extract_diff_eq()
            self.diff_eq.solve()
            self.diff_eq.record_solution("outputs/" + self.file_name)
        except Exception as err:
            messagebox.showinfo("Differential Equation Solver", err)
            return
        messagebox.showinfo("Differential Equation Solver", "Your solution has been recorded")
        self.fig.clf()
        self.diff_eq.display(self.fig)
        self.canvas.draw()
