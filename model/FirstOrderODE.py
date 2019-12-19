import numpy as np

from model.ODE import ODE


class FirstOrderODE(ODE):
    initial_value: float

    def __init__(self, function, initial_value: float):
        super().__init__(function)
        self.initial_value = initial_value

    def integrate(self, L: float, n: int) -> np.array:
        dx = L/n
        y = []
        y_i = self.initial_value
        for i in range(n):
            y.append(y_i)
            y_i = y_i + self.function(i*dx, y_i)*dx
        return np.array(y)