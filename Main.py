from exception.BoundaryTypeException import BoundaryTypeException
from model.FirstOrderODE import FirstOrderODE
from model.HeatEquation import HeatEquation
from model.SecondOrderODE import SecondOrderODE
from model.WaveEquation import WaveEquation
import matplotlib.pyplot as plt
from math import *
import tkinter as tk


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
    root.geometry("400x400")
    tk.Label(root, text="Demo").pack(side=tk.TOP, pady=20)
    tk.Button(root, text="ode1 example", command=first_order_ode_example).pack(side=tk.TOP,pady=10)
    tk.Button(root, text="ode2 example", command=second_order_ode_example).pack(side=tk.TOP, pady=10)
    tk.Button(root, text="heat example", command=heat_equation_example).pack(side=tk.TOP, pady=10)
    tk.Button(root, text="wave example", command=wave_equation_example).pack(side=tk.TOP, pady=10)
    root.mainloop()
