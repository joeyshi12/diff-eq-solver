import tkinter as tk
from tkinter import messagebox
from backend.differential_equation import InvalidQuery
from backend.heat_equation_1d import HeatEquation1D
from frontend.page import Page


class HeatEquationPage(Page):
    diff_eq: HeatEquation1D
    solve_button: tk.Button
    display_button: tk.Button
    display_3d_button: tk.Button
    reset_button: tk.Button

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        param_ids = ["left_type", "right_type", "left_values", "right_values",
                     "initial_condition", "source", "alpha", "length", "time", "samples"]
        param_names = ["Left boundary type", "Right boundary type", "Left boundary values", "Right boundary values",
                       "Initial values", "Source term (optional)", "Diffusivity", "Length", "Time interval", "Samples"]
        param_symbols = [None, None, "\u03C6₁(t)", "\u03C6₂(t)",
                         "u(0, x)", "s(t, x)", "\u03B1", "L", "T", "N"]
        self.entries = {param_ids[i]: tk.Entry(self, font=self.font, width=25) for i in range(2, len(param_ids))}
        self.entries["left_type"] = tk.StringVar(value="D")
        self.entries["right_type"] = tk.StringVar(value="D")
        for i in range(len(param_names)):
            tk.Label(self, text=param_names[i] + ":", font=self.font,
                     background=self.bgcolor).grid(row=i, column=0, padx=18, pady=5, sticky="w")
            if param_symbols[i]:
                tk.Label(self, text=param_symbols[i] + " = ", font=self.font,
                         background=self.bgcolor).grid(row=i, column=1, pady=5, sticky="e")
                self.entries[param_ids[i]].grid(row=i, column=2)
        tk.Radiobutton(self, text="Dirichlet", font=self.font, background=self.bgcolor, activebackground=self.bgcolor,
                       variable=self.entries["left_type"], value="D").grid(row=0, column=1, sticky="w")
        tk.Radiobutton(self, text="Neumann", font=self.font, background=self.bgcolor, activebackground=self.bgcolor,
                       variable=self.entries["left_type"], value="N").grid(row=0, column=2, sticky="w")
        tk.Radiobutton(self, text="Dirichlet", font=self.font, background=self.bgcolor, activebackground=self.bgcolor,
                       variable=self.entries["right_type"], value="D").grid(row=1, column=1, sticky="w")
        tk.Radiobutton(self, text="Neumann", font=self.font, background=self.bgcolor, activebackground=self.bgcolor,
                       variable=self.entries["right_type"], value="N").grid(row=1, column=2, sticky="w")
        self.solve_button = tk.Button(self, text="Solve", font=self.font, width=10, command=self.solve)
        self.solve_button.grid(row=10, column=2, pady=5, sticky="w")
        self.reset_button = tk.Button(self, text="Reset", font=self.font, width=10, command=self.reset)
        self.reset_button.grid(row=11, column=2, sticky="w")

    def solve(self):
        try:
            query = {"alpha": float(self.entries["alpha"].get()),
                     "length": float(self.entries["length"].get()),
                     "time": float(self.entries["time"].get()),
                     "samples": int(self.entries["samples"].get()),
                     "boundary_condition": {"left": {"type": self.entries["left_type"].get(),
                                                     "values": self.entries["left_values"].get()},
                                            "right": {"type": self.entries["right_type"].get(),
                                                      "values": self.entries["right_values"].get()}},
                     "initial_condition": self.entries["initial_condition"].get()}
            if self.entries["source"].get():
                query["source"] = self.entries["source"].get()
            self.diff_eq = HeatEquation1D(query)
        except ValueError or InvalidQuery:
            messagebox.showinfo("Differential Equation Solver", "Invalid value encountered in one of the entries")
            return

        self.diff_eq.solve()
        self.diff_eq.record_solution("../outputs/heat_eq_1d.xlsx")
        messagebox.showinfo("Differential Equation Solver",
                            "Your solution has been written in outputs/heat_eq_1d.xlsx")
        self.solve_button.destroy()
        self.display_button = tk.Button(self, text="Display", font=self.font, width=10, command=self.diff_eq.display)
        self.display_button.grid(row=10, column=2, pady=5, sticky="w")
        self.display_3d_button = tk.Button(self, text="Display 3D", font=self.font, width=10,
                                           command=self.diff_eq.display_3d_plot)
        self.display_3d_button.grid(row=11, column=2, pady=(0, 5), sticky="w")
        self.reset_button.grid(row=12)

    def reset(self):
        self.display_button.destroy()
        self.display_3d_button.destroy()
        self.solve_button = tk.Button(self, text="Solve", font=self.font, width=10, command=self.solve)
        self.solve_button.grid(row=10, column=2, pady=5, sticky="w")
        self.reset_button.grid(row=11)
