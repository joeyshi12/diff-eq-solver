import numpy as np

from model.ODE import ODE


class SecondOrderODE(ODE):
    initial_value: float
    initial_derivative: float

    def __init__(self, function, initial_value: float, initial_derivative: float):
        super().__init__(function)
        self.initial_value = initial_value
        self.initial_derivative = initial_derivative

    def integrate(self, L: float, n: int) -> np.array:
        dx = L / n
        y = []
        y_i_prime = self.initial_derivative
        y_i = self.initial_value
        for i in range(n):
            y.append(y_i)
            y_i_prime = y_i_prime + self.function(i * dx, y_i, y_i_prime) * dx
            y_i = y_i + y_i_prime * dx
        return np.array(y)
