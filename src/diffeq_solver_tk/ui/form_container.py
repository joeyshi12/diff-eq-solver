import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from diffeq_solver_tk.ui.forms import DifferentialEquationForm, FirstOrderODEForm, SecondOrderODEForm, HeatEquationForm, WaveEquationForm
from diffeq_solver_tk.diffeq import OrdinaryDifferentialEquationService, BoundedEquationService, \
    solve_first_order_ode, solve_second_order_ode, solve_heat_equation, solve_wave_equation

class FormContainer(tk.Frame):
    def __init__(self, master: tk.Frame, canvas: FigureCanvasTkAgg):
        tk.Frame.__init__(self, master=master)

        form_frame = tk.Frame(self)
        first_order_ode_form = FirstOrderODEForm(form_frame, canvas,
            OrdinaryDifferentialEquationService(solve_first_order_ode, canvas.figure))
        second_order_ode_form = SecondOrderODEForm(form_frame, canvas,
            OrdinaryDifferentialEquationService(solve_second_order_ode, canvas.figure))
        heat_equation_form = HeatEquationForm(form_frame, canvas,
            BoundedEquationService(solve_heat_equation, canvas.figure))
        wave_equation_form = WaveEquationForm(form_frame, canvas,
            BoundedEquationService(solve_wave_equation, canvas.figure))
        form_frame.pack(side="bottom", fill="both", expand=True)
        first_order_ode_form.place(x=0, relwidth=1, relheight=1)
        second_order_ode_form.place(x=0, relwidth=1, relheight=1)
        heat_equation_form.place(x=0, relwidth=1, relheight=1)
        wave_equation_form.place(x=0, relwidth=1, relheight=1)
        self.selected_form = first_order_ode_form

        navbar_frame = tk.Frame(self)
        navbar_frame.pack(side="top", fill="x")
        tk.Button(navbar_frame, padx=4, text="First Order ODE", command=lambda: self.select_form(first_order_ode_form)).grid(row=0, column=0)
        tk.Button(navbar_frame, padx=4, text="Second Order ODE", command=lambda: self.select_form(second_order_ode_form)).grid(row=0, column=1)
        tk.Button(navbar_frame, padx=4, text="Heat Equation", command=lambda: self.select_form(heat_equation_form)).grid(row=0, column=2)
        tk.Button(navbar_frame, padx=4, text="Wave Equation", command=lambda: self.select_form(wave_equation_form)).grid(row=0, column=3)

        self.selected_form.lift()


    def select_form(self, form: DifferentialEquationForm):
        if self.selected_form != form:
            self.selected_form.reset()
            self.selected_form = form
            self.selected_form.lift()
