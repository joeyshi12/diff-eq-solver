import tkinter as tk

from ui.FirstOrderODEPage import FirstOrderODEPage
from ui.HeatEquationPage import HeatEquationPage
from ui.SecondOrderODEPage import SecondOrderODEPage
from ui.WaveEquationPage import WaveEquationPage


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = FirstOrderODEPage(self)
        p2 = SecondOrderODEPage(self)
        p3 = HeatEquationPage(self)
        p4 = WaveEquationPage(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="First Order ODE", command=p1.lift, width=16)
        b2 = tk.Button(buttonframe, text="Second Order ODE", command=p2.lift, width=16)
        b3 = tk.Button(buttonframe, text="Heat Equation", command=p3.lift, width=16)
        b4 = tk.Button(buttonframe, text="Wave Equation", command=p4.lift, width=16)

        b1.grid(row=0, column=0)
        b2.grid(row=0, column=1)
        b3.grid(row=0, column=2)
        b4.grid(row=0, column=3)

        p1.show()