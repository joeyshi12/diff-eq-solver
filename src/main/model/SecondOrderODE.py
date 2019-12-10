import numpy as np
import matplotlib.pyplot as plt


class SecondOrderODE:
    initial_value: float
    initial_derivative: float

    def __init__(self, function, initial_value: float, initial_derivative: float):
        self.function = function
        self.initial_value = initial_value
        self.initial_derivative = initial_derivative

    def integrate(self, L: float, n: int) -> list:
        dx = L/n
        y = []
        y0_prime = self.initial_derivative
        y0 = self.initial_value
        for i in range(n):
            y.append(y0)
            y1_prime = y0_prime + self.function(i*dx, y0, y0_prime)*dx
            y0_prime = y1_prime
            y1 = y0 + y0_prime*dx
            y0 = y1
        return y

    def plot_solution(self, L: float, n: int):
        x = np.linspace(0, L, n)
        y = self.integrate(L, n)
        plt.plot(x,y)