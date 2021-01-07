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

        self.pages = {"First Order ODE": FirstOrderODEPage(self),
                      "Second Order ODE": SecondOrderODEPage(self),
                      "Heat Equation": HeatEquationPage(self),
                      "Wave Equation": WaveEquationPage(self)}

        button_frame = tk.Frame(self)
        container = tk.Frame(self)
        container.configure(background=self.bgcolour)
        button_frame.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        for page in self.pages.values():
            page.place(in_=container, x=0, y=20, relwidth=1, relheight=1)

        buttons = [tk.Button(button_frame, text=key, font=("Arial", 10, "bold"), foreground="#FFFFFF",
                             background="#4F5D75", command=self.pages[key].show, width=16) for key in self.pages.keys()]
        for i in range(len(buttons)):
            buttons[i].grid(row=0, column=i)

        self.pages["First Order ODE"].show()

    def pause_animation(self):
        if self.pages["Heat Equation"].anim:
            self.pages["Heat Equation"].pause_animation()
        elif self.pages["Wave Equation"].anim:
            self.pages["Wave Equation"].pause_animation()
