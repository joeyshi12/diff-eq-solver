import timeit
from typing import Callable

import numpy as np
from matplotlib.figure import Figure

from diffeq_solver_tk.differential_equation_metadata import HeatEquationMetadata, BoundaryType
from diffeq_solver_tk.services.differential_equation_service import BoundedEquationService


class HeatEquationService(BoundedEquationService):
    def __init__(self, main_figure: Figure):
        super().__init__(main_figure)

    def compute_solution(self, metadata: HeatEquationMetadata) -> np.ndarray:
        start_time = timeit.default_timer()
        initial_values: Callable[[float], float] = lambda x: eval(metadata.initial_values)
        source: Callable[[float, float], float] = lambda t, x: eval(metadata.source)
        N = metadata.samples
        dx = metadata.length / (N - 1)
        K = 2 * int(2 * metadata.alpha * metadata.time / dx ** 2) + 1
        dt = metadata.time / (K - 1)
        D = self.create_time_step_matrix(metadata.alpha * dt / dx ** 2, N)
        left_values: Callable[[float], float] = lambda t: eval(metadata.boundary_conditions.left.values)
        right_values: Callable[[float], float] = lambda t: eval(metadata.boundary_conditions.right.values)
        is_left_dirichlet = metadata.boundary_conditions.left.type == BoundaryType.DIRICHLET
        is_right_dirichlet = metadata.boundary_conditions.right.type == BoundaryType.DIRICHLET

        solution = np.zeros((K, N))
        solution[0] = initial_values(np.arange(N) * dx)
        for k in range(1, K):
            T = k * dt
            solution[k, 1:N - 1] = D @ solution[k - 1]
            solution[k, 1:N - 1] += source(T, np.arange(1, N - 1) * dx) * dt
            solution[k, 0] = left_values(T) if is_left_dirichlet else solution[k, 1] - left_values(T) * dx
            solution[k, -1] = right_values(T) if is_right_dirichlet else solution[k, -2] + right_values(T) * dx

        total_time = timeit.default_timer() - start_time
        print(f"computing heat equation solution took {total_time} seconds")
        return solution

    def validate_metadata(self, metadata: HeatEquationMetadata):
        if metadata.samples <= 1 or metadata.length == 0 or metadata.time == 0:
            raise Exception("invalid heat equation metadata")

    def create_time_step_matrix(self, r: float, N: int) -> np.ndarray:
        D = np.zeros((N - 2, N))
        for i in range(N - 2):
            D[i, i] = r
            D[i, i + 1] = 1 - 2 * r
            D[i, i + 2] = r
        return D
