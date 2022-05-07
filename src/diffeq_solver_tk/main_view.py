from tkinter import RIGHT, BOTH, Tk, Frame, Button

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from diffeq_solver_tk import tkinter_config as config
from diffeq_solver_tk.forms.differential_equation_form import DifferentialEquationForm
from diffeq_solver_tk.forms.first_order_ode_form import FirstOrderODEForm
from diffeq_solver_tk.forms.heat_equation_form import HeatEquationForm
from diffeq_solver_tk.forms.second_order_ode_form import SecondOrderODEForm
from diffeq_solver_tk.forms.wave_equation_form import WaveEquationForm
from diffeq_solver_tk.services.first_order_ode_service import FirstOrderODEService
from diffeq_solver_tk.services.heat_equation_service import HeatEquationService
from diffeq_solver_tk.services.second_order_ode_service import SecondOrderODEService
from diffeq_solver_tk.services.wave_equation_service import WaveEquationService


class MainView(Frame):
    first_order_ode_form: FirstOrderODEForm
    second_order_ode_form: SecondOrderODEForm
    heat_equation_form: HeatEquationForm
    wave_equation_form: WaveEquationForm
    selected_form: DifferentialEquationForm = None

    def __init__(self, app: Tk):
        Frame.__init__(self, master=app)
        self.initialize_forms()
        self.build_nav_bar()
        self.build_details_container()
        self.handle_select_form(self.first_order_ode_form)

    def initialize_forms(self):
        figure = Figure(figsize=(6, 1), dpi=91.4)
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH)
        self.first_order_ode_form = FirstOrderODEForm(self, canvas, FirstOrderODEService(figure))
        self.second_order_ode_form = SecondOrderODEForm(self, canvas, SecondOrderODEService(figure))
        self.heat_equation_form = HeatEquationForm(self, canvas, HeatEquationService(figure))
        self.wave_equation_form = WaveEquationForm(self, canvas, WaveEquationService(figure))

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

    def place_nav_bar_button(self, frame: Frame, text: str, target_form: DifferentialEquationForm, column: int):
        Button(frame,
               text=text,
               font=config.nav_bar_font,
               foreground=config.nav_bar_foreground,
               background=config.nav_bar_background,
               command=lambda: self.handle_select_form(target_form),
               width=config.nav_bar_button_width).grid(row=0, column=column)

    def handle_select_form(self, form: DifferentialEquationForm):
        if self.selected_form == form:
            return
        if self.selected_form:
            self.selected_form.reset()
        self.selected_form = form
        self.selected_form.lift()
