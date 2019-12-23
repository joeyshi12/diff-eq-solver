import tkinter as tk

from ui.Page import Page


class HeatEquationPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        boundary_type = tk.IntVar()
        boundary_type.set(value=0)
        rb1 = tk.Radiobutton(self, text="Dirichlet", variable=boundary_type, value=0, padx=10)
        rb2 = tk.Radiobutton(self, text="Neumann", variable=boundary_type, value=1, padx=10)
        rb3 = tk.Radiobutton(self, text="Mixed 1", variable=boundary_type, value=2, padx=10)
        rb4 = tk.Radiobutton(self, text="Mixed 2", variable=boundary_type, value=3, padx=10)

        rb1.grid(row=0, column=0)
        rb2.grid(row=1, column=0)
        rb3.grid(row=2, column=0)
        rb4.grid(row=3, column=0)

        def print_rb():
            print(boundary_type.get())

        tk.Button(self, text="clickMe", command=print_rb).grid(row=4, column=0)

