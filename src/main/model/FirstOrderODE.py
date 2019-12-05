import numpy as np
import matplotlib.pyplot as plt


class FirstOrderODE:

    def __init__(self, function, initial_condition):
        self.function = function
        self. initial_condition = initial_condition

    def integrate(self, L, n):
        dx = L/n
        y = np.array([])
        y0 = self.initial_condition
        for i in range(n):
            y = np.append(y, y0)
            y1 = y0 + self.function(i*dx, y0)
            y0 = y1
        return y

    def plot_solution(self, L, n):
        x = np.linspace(0, L, n)
        y = self.integrate(L, n)
        print(x)
        plt.plot(x, y)
        plt.show()