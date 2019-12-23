from exception.BoundaryTypeException import BoundaryTypeException
from model.FirstOrderODE import FirstOrderODE
from model.HeatEquation import HeatEquation
from model.SecondOrderODE import SecondOrderODE
from model.WaveEquation import WaveEquation
import matplotlib.pyplot as plt
from math import *
import tkinter as tk

from ui.MainView import MainView


def first_order_ode_example():
    first_order_ode = FirstOrderODE(lambda x, y: y, 1)
    first_order_ode.plot_solution(10, 1000)
    first_order_ode.write_solution(10, 100)
    plt.show()


def second_order_ode_example():
    second_order_ode = SecondOrderODE(lambda x, y, y_prime: -y, 0, 1)
    second_order_ode.plot_solution(4 * pi, 100)
    second_order_ode.write_solution(4 * pi, 100)
    x1, x2, y1, y2 = plt.axis()
    plt.axis((x1, x2, -2, 2))
    plt.show()


def heat_equation_example():
    p = lambda t: 0  # Left Boundary
    q = lambda t: 0  # Right Boundary
    f = lambda x: 2 * x - x ** 2  # Initial Values
    heat_equation = HeatEquation(1, 0, p, q, f)
    L = 2
    n = 50
    t = 1
    m = heat_equation.get_stable_m(L, n, t)
    try:
        heat_equation.plot_solution(L, n, t, m)
        heat_equation.write_solution(L, n, t, m)
    except BoundaryTypeException:
        print("Invalid boundary type in heat equation")
    plt.show()


def wave_equation_example():
    p = lambda t: 0  # Left Boundary
    q = lambda t: 0  # Right Boundary
    f = lambda x: 2 * x - x ** 2  # Initial Values
    g = lambda x: 0  # Initial Derivatives
    wave_equation = WaveEquation(1, 0, p, q, f, g)
    L = 2
    n = 50
    t = 2
    m = wave_equation.get_stable_m(L, n, t)
    try:
        wave_equation.plot_solution(L, n, t, m)
        wave_equation.write_solution(L, n, t, m)
    except BoundaryTypeException:
        print("Invalid boundary type in wave equation")
    plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Differential Equation Solver")
    root.geometry("490x400")
    # tk.Label(root, text="Choose a type").pack(side=tk.TOP, pady=20)
    # ode1_button = tk.Button(root, text="First Order Ordinary Equation", command=first_order_page, width=42)
    # ode1_button.pack(side=tk.TOP,pady=10)
    # ode2_button = tk.Button(root, text="Second Order Ordinary Equation", command=second_order_page, width=42)
    # ode2_button.pack(side=tk.TOP, pady=10)
    # heat_button = tk.Button(root, text="Heat Equation", command=heat_page, width=42)
    # heat_button.pack(side=tk.TOP, pady=10)
    # wave_button = tk.Button(root, text="Wave Equation", command=wave_equation_example, width=42)
    # wave_button.pack(side=tk.TOP, pady=10)
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
