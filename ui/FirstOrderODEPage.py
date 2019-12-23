import tkinter as tk

import matplotlib.pyplot as plt
from model.FirstOrderODE import FirstOrderODE
from ui.Page import Page


class FirstOrderODEPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        tk.Label(self, text="f(x,y) = ").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self, text="y(0) = ").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self, text="L = ").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(self, text="n = ").grid(row=4, column=0, padx=10, pady=10)

        f_entry = tk.Entry(self)
        y0_entry = tk.Entry(self)
        L_entry = tk.Entry(self)
        n_entry = tk.Entry(self)

        f_entry.grid(row=1, column=1, pady=10)
        y0_entry.grid(row=2, column=1, pady=10)
        L_entry.grid(row=3, column=1, pady=10)
        n_entry.grid(row=4, column=1, pady=10)

        def plot_and_record():
            f = lambda x, y: eval(f_entry.get())
            y0 = eval(y0_entry.get())
            L = eval(L_entry.get())
            n = int(n_entry.get())
            ode = FirstOrderODE(f, y0)
            ode.plot_solution(L, n)
            ode.write_solution(L, n)
            plt.show()

        plot_button = tk.Button(self, text="plot and record solution", command=plot_and_record)
        plot_button.grid(row=5, column=1, pady=10)
