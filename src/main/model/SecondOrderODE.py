from src.main.model.ODE import ODE


class SecondOrderODE(ODE):
    initial_value: float
    initial_derivative: float

    def __init__(self, function, initial_value: float, initial_derivative: float):
        self.function = function
        self.initial_value = initial_value
        self.initial_derivative = initial_derivative

    def integrate(self, L: float, n: int) -> list:
        dx = L/n
        y = [] 
        return y