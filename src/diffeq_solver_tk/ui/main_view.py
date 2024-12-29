from tkinter import RIGHT, BOTH, Tk, Frame, Button

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import diffeq_solver_tk as detk
from diffeq_solver_tk.ui.forms import \
    DifferentialEquationForm, FirstOrderODEForm, HeatEquationForm, SecondOrderODEForm, WaveEquationForm
from diffeq_solver_tk.diffeq import \
    solve_first_order_ode, solve_second_order_ode, solve_heat_equation, solve_wave_equation, \
    OrdinaryDifferentialEquationService, BoundedEquationService

NAV_BAR_FONT = ("Arial", 10, "bold")
NAV_BAR_FOREGROUND = "#FFFFFF"
NAV_BAR_BACKGROUND = "#4F5D75"
NAV_BAR_BUTTON_WIDTH = 16


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
        self.first_order_ode_form = FirstOrderODEForm(
            self, canvas,
            OrdinaryDifferentialEquationService(solve_first_order_ode, figure))
        self.second_order_ode_form = SecondOrderODEForm(
            self, canvas,
            OrdinaryDifferentialEquationService(solve_second_order_ode, figure))
        self.heat_equation_form = HeatEquationForm(
            self, canvas,
            BoundedEquationService(solve_heat_equation, figure))
        self.wave_equation_form = WaveEquationForm(
            self, canvas,
            BoundedEquationService(solve_wave_equation, figure))

    def build_nav_bar(self):
        nav_bar_frame = Frame(self)
        nav_bar_frame.pack(side="top", fill="x", expand=False)
        self.place_nav_bar_button(
            nav_bar_frame, "First Order ODE", self.first_order_ode_form, 0)
        self.place_nav_bar_button(
            nav_bar_frame, "Second Order ODE", self.second_order_ode_form, 1)
        self.place_nav_bar_button(
            nav_bar_frame, "Heat Equation", self.heat_equation_form, 2)
        self.place_nav_bar_button(
            nav_bar_frame, "Wave Equation", self.wave_equation_form, 3)

    def build_details_container(self):
        container = Frame(self)
        container.configure(background=detk.DETAILS_BACKGROUND)
        container.pack(side="top", fill="both", expand=True)
        self.first_order_ode_form.place(
            in_=container, x=0, y=detk.DETAILS_TOP_MARGIN, relwidth=1, relheight=1)
        self.second_order_ode_form.place(
            in_=container, x=0, y=detk.DETAILS_TOP_MARGIN, relwidth=1, relheight=1)
        self.heat_equation_form.place(
            in_=container, x=0, y=detk.DETAILS_TOP_MARGIN, relwidth=1, relheight=1)
        self.wave_equation_form.place(
            in_=container, x=0, y=detk.DETAILS_TOP_MARGIN, relwidth=1, relheight=1)

    def place_nav_bar_button(self, frame: Frame, text: str, target_form: DifferentialEquationForm, column: int):
        Button(frame,
               text=text,
               font=NAV_BAR_FONT,
               foreground=NAV_BAR_FOREGROUND,
               background=NAV_BAR_BACKGROUND,
               command=lambda: self.handle_select_form(target_form),
               width=NAV_BAR_BUTTON_WIDTH).grid(row=0, column=column)

    def handle_select_form(self, form: DifferentialEquationForm):
        if self.selected_form == form:
            return
        if self.selected_form:
            self.selected_form.reset()
        self.selected_form = form
        self.selected_form.lift()
