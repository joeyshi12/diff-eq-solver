from tkinter import RIGHT, BOTH
from tkinter.ttk import Button, Frame

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.differential_equation_form import DifferentialEquationForm
from src.first_order_ode.first_order_ode_form import FirstOrderODEForm
from src.heat_equation.heat_equation_form import HeatEquationForm
from src.second_order_ode.second_order_ode_form import SecondOrderODEForm
from src.wave_equation.wave_equation_form import WaveEquationForm


class MainView(Frame):
    bgcolour: str = '#BFC0C0'

    def __init__(self, window):
        Frame.__init__(self, master=window)
        self.figure = Figure(figsize=(6, 1), dpi=91.4)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH)
        nav_bar_frame = Frame(self)
        nav_bar_frame.pack(side="top", fill="x", expand=False)
        container = Frame(self)
        container.configure(background=self.bgcolour)
        container.pack(side="top", fill="both", expand=True)

        self.first_order_ode_form = FirstOrderODEForm(self)
        self.second_order_ode_form = SecondOrderODEForm(self)
        self.heat_equation_form = HeatEquationForm(self)
        self.wave_equation_form = WaveEquationForm(self)

        self.first_order_ode_form.place(in_=container, x=0, y=20, relwidth=1, relheight=1)
        self.second_order_ode_form.place(in_=container, x=0, y=20, relwidth=1, relheight=1)
        self.heat_equation_form.place(in_=container, x=0, y=20, relwidth=1, relheight=1)
        self.wave_equation_form.place(in_=container, x=0, y=20, relwidth=1, relheight=1)

        self.initialize_nav_bar(nav_bar_frame)
        self.first_order_ode_form.show()

    def initialize_nav_bar(self, nav_bar_frame: Frame):
        font = ("Arial", 10, "bold")
        Button(
            nav_bar_frame,
            text="First Order ODE",
            font=font,
            foreground="#FFFFFF",
            background="#4F5D75",
            command=lambda: self.switch_form(self.first_order_ode_form),
            width=16
        ).grid(row=0, column=0)
        Button(
            nav_bar_frame,
            text="Second Order ODE",
            font=font,
            foreground="#FFFFFF",
            background="#4F5D75",
            command=lambda: self.switch_form(self.second_order_ode_form),
            width=16
        ).grid(row=0, column=1)
        Button(
            nav_bar_frame,
            text="Heat Equation",
            font=font,
            foreground="#FFFFFF",
            background="#4F5D75",
            command=lambda: self.switch_form(self.heat_equation_form),
            width=16
        ).grid(row=0, column=2)
        Button(
            nav_bar_frame,
            text="Wave Equation",
            font=font,
            foreground="#FFFFFF",
            background="#4F5D75",
            command=lambda: self.switch_form(self.wave_equation_form),
            width=16
        ).grid(row=0, column=3)

    def switch_form(self, form: DifferentialEquationForm):
        self.figure.clf()
        form.lift()

    def clear_canvas(self):
        self.heat_equation_form.clear_form()
        self.wave_equation_form.clear_form()
