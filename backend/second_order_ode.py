import numpy as np
from numpy import sin, cos, sinh, cosh, exp, e, pi
from backend.differential_equation import ODE, InvalidQuery


class SecondOrderODE(ODE):
    def __init__(self, query):
        if not self.is_valid(query):
            raise InvalidQuery("received invalid query")
        N = query["samples"]
        self.dt = query["time"] / (N - 1)
        self.derivative = query["initial_derivative"]
        self.source = lambda t, x, y: eval(query["source"])
        self.solution = np.zeros(N)
        self.solution[0] = query["initial_value"]

    def is_valid(self, query):
        return query["samples"] > 1 and query["time"] > 0

    def solve(self):
        N = self.solution.size
        for i in range(1, N):
            self.derivative = self.derivative + self.source((i - 1) * self.dt, self.solution[i - 1], self.derivative) * self.dt
            self.solution[i] = self.solution[i - 1] + self.derivative * self.dt
