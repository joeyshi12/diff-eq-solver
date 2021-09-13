import numpy as np
from src.differential_equation_metadata import WaveEquationMetadata
from src.differential_equation import BoundedEquation


class WaveEquation(BoundedEquation):
    metadata: WaveEquationMetadata

    def __init__(self, metadata: WaveEquationMetadata):
        super().__init__(metadata)
        initial_values: '(x: float) -> float' = lambda x: eval(metadata.initial_values)
        initial_derivatives: '(x: float) -> float' = lambda x: eval(metadata.initial_derivatives)
        self.source = lambda t, x: eval(metadata.source)
        N = metadata.samples
        self.dx = metadata.length / (N - 1)
        K = 2 * np.int(metadata.c * metadata.time / self.dx) + 1
        self.dt = metadata.time / (K - 1)
        self.D = self.create_time_step_matrix()

        # Initialize solution array
        self.solution = np.zeros((K, N))
        self.solution[0] = initial_values(np.arange(N) * self.dx)
        self.solution[1, 1:N - 1] = (1 / 2) * self.D @ self.solution[0]
        self.solution[1, 1:N - 1] += self.dt ** 2 * initial_derivatives(np.arange(1, N - 1) * self.dx)
        self.solution[1, 1:N - 1] += (self.dt ** 2 / 2) * self.source(self.dt, np.arange(1, N - 1) * self.dx)
        self.fill_boundary_values(1)

    def validate_metadata(self, metadata: WaveEquationMetadata):
        if metadata.samples <= 1 or metadata.length == 0 or metadata.time == 0:
            raise Exception("invalid wave equation metadata")

    def compute_solution(self):
        K, N = self.solution.shape
        for k in range(2, K):
            self.solution[k, 1:N - 1] = self.D @ self.solution[k - 1] - self.solution[k - 2, 1:N - 1]
            self.solution[k, 1:N - 1] += self.dt ** 2 * self.source(k * self.dt, np.arange(1, N - 1) * self.dx)
            self.fill_boundary_values(k)

    def create_time_step_matrix(self) -> np.ndarray:
        N = self.metadata.samples
        r = (self.metadata.c * self.dt / self.dx) ** 2
        D = np.zeros((N - 2, N))
        for i in range(N - 2):
            D[i, i] = r
            D[i, i + 1] = 2 * (1 - r)
            D[i, i + 2] = r
        return D
