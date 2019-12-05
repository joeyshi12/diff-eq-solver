import numpy as np
import matplotlib.pyplot as plt


class FirstOrderODE:

    def __init__(self, function, initial_value):
        self.function = function
        self.initial_value = initial_value

    def integrate(self, L, n):
        dx = L/n
        y = np.array([])
        y0 = self.initial_value
        for i in range(n):
            y = np.append(y, y0)
            y1 = y0 + self.function(i*dx, y0)*dx
            y0 = y1
        return y

    def plot_solution(self, L, n):
        x = np.linspace(0, L, n)
        y = self.integrate(L, n)
        plt.plot(x, y)