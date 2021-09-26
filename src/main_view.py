from tkinter import RIGHT, BOTH, Tk, Frame, Button

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import src.tkinter_config as config
from src.differential_equation_form import DifferentialEquationForm
from src.first_order_ode.first_order_ode_form import FirstOrderODEForm
from src.first_order_ode.first_order_ode_service import FirstOrderODEService
from src.heat_equation.heat_equation_form import HeatEquationForm
from src.heat_equation.heat_equation_service import HeatEquationService
from src.second_order_ode.second_order_ode_form import SecondOrderODEForm
from src.second_order_ode.second_order_ode_service import SecondOrderODEService
from src.wave_equation.wave_equation_form import WaveEquationForm
from src.wave_equation.wave_equation_service import WaveEquationService


class MainView(Frame):
    def __init__(self, app: Tk):
        Frame.__init__(self, master=app)
        self.figure = Figure(figsize=(6, 1), dpi=91.4)
        canvas = FigureCanvasTkAgg(self.figure, self)
        canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH)

        self.first_order_ode_form = FirstOrderODEForm(self, canvas, FirstOrderODEService(self.figure))
        self.second_order_ode_form = SecondOrderODEForm(self, canvas, SecondOrderODEService(self.figure))
        self.heat_equation_form = HeatEquationForm(self, canvas, HeatEquationService(self.figure))
        self.wave_equation_form = WaveEquationForm(self, canvas, WaveEquationService(self.figure))

        self.build_nav_bar()
        self.build_details_container()
        self.first_order_ode_form.show()

    def build_nav_bar(self):
        nav_bar_frame = Frame(self)
        nav_bar_frame.pack(side="top", fill="x", expand=False)
        self.place_nav_bar_button(nav_bar_frame, "First Order ODE", self.first_order_ode_form, 0)
        self.place_nav_bar_button(nav_bar_frame, "Second Order ODE", self.second_order_ode_form, 1)
        self.place_nav_bar_button(nav_bar_frame, "Heat Equation", self.heat_equation_form, 2)
        self.place_nav_bar_button(nav_bar_frame, "Wave Equation", self.wave_equation_form, 3)

    def build_details_container(self):
        container = Frame(self)
        container.configure(background=config.details_background)
        container.pack(side="top", fill="both", expand=True)
        self.first_order_ode_form.place(in_=container, x=0, y=config.details_top_margin, relwidth=1, relheight=1)
        self.second_order_ode_form.place(in_=container, x=0, y=config.details_top_margin, relwidth=1, relheight=1)
        self.heat_equation_form.place(in_=container, x=0, y=config.details_top_margin, relwidth=1, relheight=1)
        self.wave_equation_form.place(in_=container, x=0, y=config.details_top_margin, relwidth=1, relheight=1)

    def place_nav_bar_button(self, frame: Frame, display_name: str, target_form: DifferentialEquationForm, column: int):
        Button(frame,
               text=display_name,
               font=config.nav_bar_font,
               foreground=config.nav_bar_foreground,
               background=config.nav_bar_background,
               command=lambda: self.switch_form(target_form),
               width=config.nav_bar_button_width).grid(row=0, column=column)

    def switch_form(self, form: DifferentialEquationForm):
        self.figure.clf()
        form.lift()

    def clear_canvas(self):
        self.heat_equation_form.clear_form()
