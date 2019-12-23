import tkinter as tk
import matplotlib.pyplot as plt

from math import *
from model.HeatEquation import HeatEquation
from ui.Page import Page


class HeatEquationPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        boundary_type_variable = tk.IntVar()
        boundary_type_variable.set(value=0)
        rb1 = tk.Radiobutton(self, text="Dirichlet", variable=boundary_type_variable, value=0, padx=10)
        rb2 = tk.Radiobutton(self, text="Neumann", variable=boundary_type_variable, value=1, padx=10)
        rb3 = tk.Radiobutton(self, text="Mixed 1", variable=boundary_type_variable, value=2, padx=10)
        rb4 = tk.Radiobutton(self, text="Mixed 2", variable=boundary_type_variable, value=3, padx=10)

        rb1.grid(row=0, column=1)
        rb2.grid(row=1, column=1)
        rb3.grid(row=2, column=1)
        rb4.grid(row=3, column=1)

        tk.Label(self, text="alpha = ").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(self, text="p(t) = ").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(self, text="q(t) = ").grid(row=6, column=0, padx=10, pady=10)
        tk.Label(self, text="f(x) = ").grid(row=7, column=0, padx=10, pady=10)
        tk.Label(self, text="L = ").grid(row=4, column=2, padx=10, pady=10)
        tk.Label(self, text="t = ").grid(row=5, column=2, padx=10, pady=10)
        tk.Label(self, text="n = ").grid(row=6, column=2, padx=10, pady=10)

        alpha_entry = tk.Entry(self)
        p_entry = tk.Entry(self)
        q_entry = tk.Entry(self)
        f_entry = tk.Entry(self)
        L_entry = tk.Entry(self)
        t_entry = tk.Entry(self)
        n_entry = tk.Entry(self)

        alpha_entry.grid(row=4, column=1, pady=10)
        p_entry.grid(row=5, column=1, pady=10)
        q_entry.grid(row=6, column=1, pady=10)
        f_entry.grid(row=7, column=1, pady=10)
        L_entry.grid(row=4, column=3, pady=10)
        t_entry.grid(row=5, column=3, pady=10)
        n_entry.grid(row=6, column=3, pady=10)

        pde = HeatEquation(0, 0, lambda x: x, lambda x: x, lambda x: x)

        def plot_and_write():
            pde.alpha = eval(alpha_entry.get())
            pde.boundary_type = int(boundary_type_variable.get())
            pde.p = lambda t: eval(p_entry.get())
            pde.q = lambda t: eval(q_entry.get())
            pde.f = lambda x: eval(f_entry.get())
            L = eval(L_entry.get())
            t = eval(t_entry.get())
            n = int(n_entry.get())
            m = int(pde.get_stable_m(L, n, t))
            pde.plot_solution(L, n, t, m)
            pde.write_solution(L, n, t, m)
            plt.show()

        record_button = tk.Button(self, text="plot and write solution", command=plot_and_write)
        record_button.grid(row=8, column=1, pady=10)
