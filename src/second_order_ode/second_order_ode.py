import numpy as np
from src.differential_equation_metadata import SecondOrderODEMetadata
from src.differential_equation import ODE


class SecondOrderODE(ODE):
    def __init__(self, metadata: SecondOrderODEMetadata):
        super().__init__(metadata)
        N = metadata.samples
        self.dt = metadata.time / (N - 1)
        self.derivative = metadata.initial_derivative
        self.source = lambda t, x, y: eval(metadata.source)
        self.solution = np.zeros(N)
        self.solution[0] = metadata.initial_value

    def validate_metadata(self, metadata: SecondOrderODEMetadata):
        if metadata.samples <= 1 or metadata.time == 0:
            raise Exception("invalid second order ode metadata")

    def compute_solution(self):
        N = self.solution.size
        for i in range(1, N):
            derivative_step = self.source((i - 1) * self.dt, self.solution[i - 1], self.derivative) * self.dt
            self.derivative = self.derivative + derivative_step
            self.solution[i] = self.solution[i - 1] + self.derivative * self.dt
