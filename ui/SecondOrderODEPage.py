import tkinter as tk

from model.SecondOrderODE import SecondOrderODE
from ui.Page import Page
import matplotlib.pyplot as plt


class SecondOrderODEPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        tk.Label(self, text="f(x,y,z) = ").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self, text="y(0) = ").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self, text="z(0) = ").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(self, text="L = ").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(self, text="n = ").grid(row=5, column=0, padx=10, pady=10)

        f_entry = tk.Entry(self)
        y0_entry = tk.Entry(self)
        z0_entry = tk.Entry(self)
        L_entry = tk.Entry(self)
        n_entry = tk.Entry(self)

        f_entry.grid(row=1, column=1, pady=10)
        y0_entry.grid(row=2, column=1, pady=10)
        z0_entry.grid(row=3, column=1, pady=10)
        L_entry.grid(row=4, column=1, pady=10)
        n_entry.grid(row=5, column=1, pady=10)

        ode = SecondOrderODE(lambda x, y, z: x, 0, 0)

        def plot_and_write():
            ode.function = lambda x, y, z: eval(f_entry.get())
            ode.initial_value = eval(y0_entry.get())
            ode.initial_derivative = eval(z0_entry.get())
            L = eval(L_entry.get())
            n = int(n_entry.get())
            ode.plot_solution(L, n)
            ode.write_solution(L, n)
            plt.show()

        record_button = tk.Button(self, text="plot and write solution", command=plot_and_write)
        record_button.grid(row=6, column=1, pady=10)
