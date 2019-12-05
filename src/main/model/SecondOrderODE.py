import numpy as np
import matplotlib.pyplot as plt


class SecondOrderODE:

    def __init__(self, function, initial_value, initial_derivative):
        self.function = function
        self.initial_value = initial_value
        self.initial_derivative = initial_derivative

    def integrate(self, L, n):
        dx = L/n
        y = np.array([])
        y0_prime = self.initial_derivative
        y0 = self.initial_value
        for i in range(n):
            y = np.append(y, y0)
            y1_prime = y0_prime + self.function(i*dx, y0, y0_prime)*dx
            y0_prime = y1_prime
            y1 = y0 + y0_prime*dx
            y0 = y1
        return y

    def plot_solution(self, L, n):
        x = np.linspace(0, L, n)
        y = self.integrate(L, n)
        plt.plot(x,y)