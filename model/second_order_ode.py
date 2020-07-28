import numpy as np

from model.ode import ODE


class SecondOrderODE(ODE):
    def __init__(self, f, initial_value, initial_derivative):
        super().__init__(f, "SecondOrderODESolution.xlsx")
        self.initial_value = initial_value
        self.initial_derivative = initial_derivative

    def solve(self, t, n):
        """computes solution into y as an array of size n+1"""
        dt = t / n
        self.t_data = np.arange(n + 1) * dt
        self.y = np.zeros(n + 1)
        y_prime = np.zeros(n + 1)
        y_prime[0] = self.initial_derivative
        self.y[0] = self.initial_value
        for i in range(1, n + 1):
            y_prime[i] = y_prime[i - 1] + self.f(i * dt, self.y[i - 1], y_prime[i - 1]) * dt
            self.y[i] = self.y[i - 1] + (y_prime[i] + y_prime[i - 1]) * dt / 2
