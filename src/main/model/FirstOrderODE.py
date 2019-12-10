import numpy as np

from src.main.model.ODE import ODE


class FirstOrderODE(ODE):
    initial_value: float

    def __init__(self, function, initial_value: float):
        self.function = function
        self.initial_value = initial_value

    def integrate(self, L: float, n: int) -> np.array:
        dx = L/n
        y = []
        y0 = self.initial_value
        for i in range(n):
            y.append(y0)
            y1 = y0 + self.function(i*dx, y0)*dx
            y0 = y1
        return np.array(y)