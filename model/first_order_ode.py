import numpy as np
from model.ode import ODE


class FirstOrderODE(ODE):
    def __init__(self, f, initial_value=0):
        super().__init__(f, "first_order_ode_solution.xlsx")
        self.initial_value = initial_value

    def solve(self, t, n):
        """computes solution into y as an array of size n+1"""
        dt = t / n
        self.t_data = np.arange(n + 1) * dt
        self.y = np.zeros(n + 1)
        self.y[0] = self.initial_value
        for i in range(1, n + 1):
            self.y[i] = self.y[i - 1] + self.f(i * dt, self.y[i - 1]) * dt
