import tkinter as tk
from tkinter import messagebox
from backend.heat_equation_1d import HeatEquation1D
from frontend.page import Page


class HeatEquationPage(Page):
    diff_eq: HeatEquation1D = None
    entries: dict
    solve_button: tk.Button
    display_button: tk.Button
    animate_button: tk.Button
    play_button: tk.Button
    pause_button: tk.Button
    file_name: str = "heat_equation_1d.xlsx"
    anim = None

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
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
        param_symbols = [None, None, "\u03C6₁(t)", "\u03C6₂(t)", "u(0, x)", "s(t, x)", "\u03B1", "L", "T", "N"]
        self.place_labels_and_entries(param_ids, param_names, param_symbols)
        self.place_radio_buttons()
        self.place_buttons()

    def place_labels_and_entries(self, param_ids, param_names, param_symbols):
        self.entries = {param_ids[i]: tk.Entry(self, font=self.font, width=24) for i in range(2, len(param_ids))}
        self.entries["left_type"] = tk.StringVar(value="D")
        self.entries["right_type"] = tk.StringVar(value="D")
        for i in range(len(param_names)):
            tk.Label(self, text=param_names[i] + ":", font=self.font,
                     background=self.bgcolour).grid(row=i, column=0, padx=18, pady=6, sticky="w")
            if param_symbols[i]:
                tk.Label(self, text=param_symbols[i] + " = ", font=self.font,
                         background=self.bgcolour).grid(row=i, column=1, pady=6, sticky="e")
                self.entries[param_ids[i]].grid(row=i, column=2, columnspan=2)

    def place_radio_buttons(self):
        tk.Radiobutton(self, text="Dirichlet", font=self.font, background=self.bgcolour, activebackground=self.bgcolour,
                       variable=self.entries["left_type"], value="D").grid(row=0, column=1, sticky="w")
        tk.Radiobutton(self, text="Neumann", font=self.font, background=self.bgcolour, activebackground=self.bgcolour,
                       variable=self.entries["left_type"], value="N").grid(row=0, column=2, sticky="w")
        tk.Radiobutton(self, text="Dirichlet", font=self.font, background=self.bgcolour, activebackground=self.bgcolour,
                       variable=self.entries["right_type"], value="D").grid(row=1, column=1, sticky="w")
        tk.Radiobutton(self, text="Neumann", font=self.font, background=self.bgcolour, activebackground=self.bgcolour,
                       variable=self.entries["right_type"], value="N").grid(row=1, column=2, sticky="w")

    def place_buttons(self):
        self.solve_button = tk.Button(self, text="Solve", font=self.font, width=10, command=self.solve)
        self.solve_button.grid(row=10, column=2, pady=6, sticky="w")
        self.display_button = tk.Button(self, text="Display", font=self.font, width=10)
        self.animate_button = tk.Button(self, text="Animate", font=self.font, width=10)
        self.play_button = tk.Button(self, text="Play", font=self.font, width=10, command=self.play_animation)
        self.pause_button = tk.Button(self, text="Pause", font=self.font, width=10, command=self.pause_animation)

    def extract_diff_eq(self):
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
        return HeatEquation1D(query)

    def solve(self):
        try:
            self.diff_eq = self.extract_diff_eq()
            self.diff_eq.solve()
            self.diff_eq.record_solution("outputs/" + self.file_name)
        except Exception as err:
            messagebox.showinfo("Differential Equation Solver", err)
            return
        messagebox.showinfo("Differential Equation Solver", "Your solution has been recorded")
        self.display_button.configure(command=self.display)
        self.display_button.grid(row=10, column=3, pady=6, sticky="e")
        self.animate_button.configure(command=self.get_animation)
        self.animate_button.grid(row=11, column=3, pady=6, sticky="e")
        self.display()

    def display(self):
        if self.anim:
            self.pause_animation()
        self.fig.clf()
        self.animate_button.configure(command=self.get_animation)
        self.animate_button.grid(row=11, column=3, pady=6, sticky="e")
        self.diff_eq.display(self.fig)
        self.canvas.draw()
        self.play_button.grid_forget()
        self.pause_button.grid_forget()

    def get_animation(self):
        self.fig.clf()
        self.anim = self.diff_eq.get_animation(self.fig)
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

    def reset(self):
        if self.anim:
            self.pause_animation()
        if self.diff_eq:
            self.play_button.grid_forget()
            self.animate_button.grid(row=11, column=3, pady=6, sticky="e")
            self.fig.clf()
            self.canvas.draw()
