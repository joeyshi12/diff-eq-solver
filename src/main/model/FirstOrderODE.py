import numpy as np
import matplotlib.pyplot as plt


class FirstOrderODE:
    initial_value: float

    def __init__(self, function, initial_value: float):
        self.function = function
        self.initial_value = initial_value

    def integrate(self, L: float, n: int) -> list:
        dx = L/n
        y = []
        y0 = self.initial_value
        for i in range(n):
            y.append(y0)
            y1 = y0 + self.function(i*dx, y0)*dx
            y0 = y1
        return y

    def plot_solution(self, L: float, n: int):
        x = np.linspace(0, L, n)
        y = self.integrate(L, n)
        plt.plot(x, y)