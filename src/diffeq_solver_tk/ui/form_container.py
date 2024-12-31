import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from diffeq_solver_tk.ui.forms import DifferentialEquationForm, FirstOrderODEForm, SecondOrderODEForm, HeatEquationForm, WaveEquationForm
from diffeq_solver_tk.diffeq import OrdinaryDifferentialEquationService, BoundedEquationService, \
    solve_first_order_ode, solve_second_order_ode, solve_heat_equation, solve_wave_equation

class FormContainer(tk.Frame):
    def __init__(self, master: tk.Frame, canvas: FigureCanvasTkAgg):
        tk.Frame.__init__(self, master=master)

        first_order_ode_form = FirstOrderODEForm(self, canvas,
            OrdinaryDifferentialEquationService(solve_first_order_ode, canvas.figure))
        second_order_ode_form = SecondOrderODEForm(self, canvas,
            OrdinaryDifferentialEquationService(solve_second_order_ode, canvas.figure))
        heat_equation_form = HeatEquationForm(self, canvas,
            BoundedEquationService(solve_heat_equation, canvas.figure))
        wave_equation_form = WaveEquationForm(self, canvas,
            BoundedEquationService(solve_wave_equation, canvas.figure))
        self.selected_form = first_order_ode_form

        navbar_frame = tk.Frame(self)
        navbar_frame.pack(side="top", fill="x")
        tk.Button(navbar_frame, text="First Order ODE", command=lambda: self.select_form(first_order_ode_form)).grid(row=0, column=0)
        tk.Button(navbar_frame, text="Second Order ODE", command=lambda: self.select_form(second_order_ode_form)).grid(row=0, column=1)
        tk.Button(navbar_frame, text="Heat Equation", command=lambda: self.select_form(heat_equation_form)).grid(row=0, column=2)
        tk.Button(navbar_frame, text="Wave Equation", command=lambda: self.select_form(wave_equation_form)).grid(row=0, column=3)

        form_frame = tk.Frame(self)
        form_frame.pack(side="bottom", fill="both", expand=True)
        first_order_ode_form.place(in_=form_frame, x=0, relwidth=1, relheight=1)
        second_order_ode_form.place(in_=form_frame, x=0, relwidth=1, relheight=1)
        heat_equation_form.place(in_=form_frame, x=0, relwidth=1, relheight=1)
        wave_equation_form.place(in_=form_frame, x=0, relwidth=1, relheight=1)
        self.selected_form.lift()


    def select_form(self, form: DifferentialEquationForm):
        if self.selected_form != form:
            self.selected_form.reset()
            self.selected_form = form
            self.selected_form.lift()
