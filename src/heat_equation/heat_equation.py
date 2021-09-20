from typing import Callable

import numpy as np
from src.differential_equation_metadata import HeatEquationMetadata
from src.differential_equation import BoundedEquation


class HeatEquation(BoundedEquation):
    metadata: HeatEquationMetadata

    def __init__(self, metadata: HeatEquationMetadata):
        super().__init__(metadata)
        initial_cond: Callable[[float], float] = lambda x: eval(metadata.initial_values)
        self.source = lambda t, x: eval(metadata.source)
        N = metadata.samples
        self.dx = metadata.length / (N - 1)
        K = 2 * np.int(2 * metadata.alpha * metadata.time / self.dx ** 2) + 1
        self.dt = metadata.time / (K - 1)
        self.D = self.create_time_step_matrix()

        # Initialize solution array
        self.solution = np.zeros((K, N))
        self.solution[0] = initial_cond(np.arange(N) * self.dx)

    def validate_metadata(self, metadata: HeatEquationMetadata):
        if metadata.samples <= 1 or metadata.length == 0 or metadata.time == 0:
            raise Exception("invalid heat equation metadata")

    def compute_solution(self):
        K, N = self.solution.shape
        for k in range(1, K):
            self.solution[k, 1:N - 1] = self.D @ self.solution[k - 1]
            self.solution[k, 1:N - 1] += self.source(k * self.dt, np.arange(1, N - 1) * self.dx) * self.dt
            self.fill_boundary_values(k)

    def create_time_step_matrix(self) -> np.ndarray:
        N = self.metadata.samples
        r = self.metadata.alpha * self.dt / self.dx ** 2
        D = np.zeros((N - 2, N))
        for i in range(N - 2):
            D[i, i] = r
            D[i, i + 1] = 1 - 2 * r
            D[i, i + 2] = r
        return D
