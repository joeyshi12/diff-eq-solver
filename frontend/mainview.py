import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from frontend.first_order_ode_page import FirstOrderODEPage
from frontend.heat_equation_page import HeatEquationPage
from frontend.second_order_ode_page import SecondOrderODEPage
from frontend.wave_equation_page import WaveEquationPage


class MainView(tk.Frame):
    bgcolour: str = '#BFC0C0'

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.fig = Figure(figsize=(6, 1), dpi=91.4)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)

        pages = {"First Order ODE": FirstOrderODEPage(self),
                 "Second Order ODE": SecondOrderODEPage(self),
                 "Heat Equation": HeatEquationPage(self),
                 "Wave Equation": WaveEquationPage(self)}

        button_frame = tk.Frame(self)
        container = tk.Frame(self)
        container.configure(background=self.bgcolour)
        button_frame.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        for page in pages.values():
            page.place(in_=container, x=0, y=20, relwidth=1, relheight=1)

        buttons = [tk.Button(button_frame, text=key, font=("Arial", 10, "bold"), foreground="#FFFFFF",
                             background="#4F5D75", command=pages[key].lift, width=16) for key in pages.keys()]
        for i in range(len(buttons)):
            buttons[i].grid(row=0, column=i)

        pages["First Order ODE"].show()
