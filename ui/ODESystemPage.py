import tkinter as tk
from tkinter import messagebox
from math import *
from model.ODESystem import ODESystem
from ui.Page import Page


class ODESystemPage(Page):
    ode: ODESystem
    solve_button: tk.Button
    reset_button: tk.Button

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        tk.Label(self, text="f(t,x,y) = ").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self, text="g(t,x,y) = ").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self, text="x(0) = ").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(self, text="y(0) = ").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(self, text="t = ").grid(row=1, column=2, padx=10, pady=10)
        tk.Label(self, text="n = ").grid(row=2, column=2, padx=10, pady=10)

        f_entry = tk.Entry(self)
        g_entry = tk.Entry(self)
        x0_entry = tk.Entry(self)
        y0_entry = tk.Entry(self)
        t_entry = tk.Entry(self)
        n_entry = tk.Entry(self)

        f_entry.grid(row=1, column=1, pady=10)
        g_entry.grid(row=2, column=1, pady=10)
        x0_entry.grid(row=3, column=1, pady=10)
        y0_entry.grid(row=4, column=1, pady=10)
        t_entry.grid(row=1, column=3, pady=10)
        n_entry.grid(row=2, column=3, pady=10)

        def reset():
            self.reset_button.destroy()
            self.solve_button.configure(text="Solve", command=solve)

        def solve():
            try:
                f = lambda t, x, y: eval(f_entry.get())
                g = lambda t, x, y: eval(g_entry.get())
                initial_x = eval(x0_entry.get())
                initial_y = eval(y0_entry.get())
                t = eval(t_entry.get())
                n = int(n_entry.get())
            except SyntaxError or ValueError:
                messagebox.showinfo("Differential Equation Solver", "Invalid value encountered in one of the entries")
                return

            self.ode = ODESystem(f, g, initial_x, initial_y)
            self.ode.solve(t, n)
            self.ode.write_solution()
            messagebox.showinfo('Differential Equation Solver',
                                'Your solution has been written in output/ODESystem.xlsx')
            self.solve_button.configure(text="Plot", command=self.ode.plot_solution)
            self.solve_button.grid(row=5, column=1, pady=10)
            self.reset_button = tk.Button(self, text="Reset", command=reset)
            self.reset_button.grid(row=7, column=1, pady=10)

        self.solve_button = tk.Button(self, text="Solve", command=solve)
        self.solve_button.grid(row=5, column=1, pady=10)
