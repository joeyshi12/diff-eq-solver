from typing import Callable

import numpy as np
from src.differential_equation_metadata import FirstOrderODEMetadata
from src.differential_equation import ODE


class FirstOrderODE(ODE):
    metadata: FirstOrderODEMetadata
    source: Callable[[float, float], float]  # (t: float, x: float) -> float

    def __init__(self, metadata: FirstOrderODEMetadata):
        super().__init__(metadata)
        N = self.metadata.samples
        self.dt = self.metadata.time / (N - 1)
        self.source = lambda t, x: eval(self.metadata.source)
        self.solution = np.zeros(N)
        self.solution[0] = self.metadata.initial_value

    def validate_metadata(self, metadata: FirstOrderODEMetadata):
        if metadata.samples <= 1 or metadata.time == 0:
            raise Exception("invalid first order ode metadata")

    def compute_solution(self):
        N = self.metadata.samples
        for i in range(1, N):
            self.solution[i] = self.solution[i - 1] + self.source(i * self.dt, self.solution[i - 1]) * self.dt
