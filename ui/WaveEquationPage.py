import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from math import *

from exception import BoundaryTypeException
from model.WaveEquation import WaveEquation
from ui.Page import Page


class WaveEquationPage(Page):
    wave_eq: WaveEquation
    solve_button: tk.Button
    animate_button: tk.Button
    reset_button: tk.Button

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        boundary_type_variable = tk.IntVar()
        boundary_type_variable.set(value=0)
        rb1 = tk.Radiobutton(self, text="Dirichlet", variable=boundary_type_variable, value=1, padx=10)
        rb2 = tk.Radiobutton(self, text="Neumann", variable=boundary_type_variable, value=2, padx=10)
        rb3 = tk.Radiobutton(self, text="Mixed 1", variable=boundary_type_variable, value=3, padx=10)
        rb4 = tk.Radiobutton(self, text="Mixed 2", variable=boundary_type_variable, value=4, padx=10)

        rb1.grid(row=0, column=1)
        rb2.grid(row=1, column=1)
        rb3.grid(row=2, column=1)
        rb4.grid(row=3, column=1)

        tk.Label(self, text="c = ").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(self, text="p(t) = ").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(self, text="q(t) = ").grid(row=6, column=0, padx=10, pady=10)
        tk.Label(self, text="f(x) = ").grid(row=7, column=0, padx=10, pady=10)
        tk.Label(self, text="g(x) = ").grid(row=7, column=2, padx=10, pady=10)
        tk.Label(self, text="L = ").grid(row=4, column=2, padx=10, pady=10)
        tk.Label(self, text="t = ").grid(row=5, column=2, padx=10, pady=10)
        tk.Label(self, text="n = ").grid(row=6, column=2, padx=10, pady=10)

        c_entry = tk.Entry(self)
        p_entry = tk.Entry(self)
        q_entry = tk.Entry(self)
        f_entry = tk.Entry(self)
        g_entry = tk.Entry(self)
        L_entry = tk.Entry(self)
        t_entry = tk.Entry(self)
        n_entry = tk.Entry(self)

        c_entry.grid(row=4, column=1, pady=10)
        p_entry.grid(row=5, column=1, pady=10)
        q_entry.grid(row=6, column=1, pady=10)
        f_entry.grid(row=7, column=1, pady=10)
        g_entry.grid(row=7, column=3, pady=10)
        L_entry.grid(row=4, column=3, pady=10)
        t_entry.grid(row=5, column=3, pady=10)
        n_entry.grid(row=6, column=3, pady=10)

        def reset():
            self.animate_button.destroy()
            self.reset_button.destroy()
            self.solve_button.configure(text="Solve", command=solve)

        def solve():
            try:
                c = eval(c_entry.get())
                boundary_type = int(boundary_type_variable.get())
                p = lambda t: eval(p_entry.get())
                q = lambda t: eval(q_entry.get())
                f = lambda x: eval(f_entry.get())
                g = lambda x: eval(g_entry.get())
                L = eval(L_entry.get())
                t = eval(t_entry.get())
                n = eval(n_entry.get())
            except SyntaxError or ValueError:
                messagebox.showinfo("Differential Equation Solver", "Invalid value encountered in one of the entries")
                return

            self.wave_eq = WaveEquation(c, boundary_type, p, q, f, g)
            m = int(self.wave_eq.get_stable_m(L, n, t))

            try:
                self.wave_eq.solve(L, n, t, m)
            except BoundaryTypeException:
                messagebox.showinfo("Differential Equation Solver", "Choose a boundary type")
                return

            self.wave_eq.write_solution()
            messagebox.showinfo('Differential Equation Solver', 'Your solution has been written in excel_data/PDE.xlsx')

            self.solve_button.configure(text="Plot", command=self.wave_eq.plot_solution)

            self.animate_button = tk.Button(self, text="Animate", command=self.wave_eq.animate_solution)
            self.animate_button.grid(row=8, column=3, pady=10)

            self.reset_button = tk.Button(self, text="Reset", command=reset)
            self.reset_button.grid(row=9, column=1, pady=10)

        self.solve_button = tk.Button(self, text="Solve", command=solve)
        self.solve_button.grid(row=8, column=1, pady=10)
