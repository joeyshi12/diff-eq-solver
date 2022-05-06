import timeit
from typing import Callable

import numpy as np
from matplotlib.figure import Figure

from diffeq_solver_tk.differential_equation_metadata import OrdinaryDifferentialEquationMetadata
from diffeq_solver_tk.services.differential_equation_service import OrdinaryDifferentialEquationService


class SecondOrderODEService(OrdinaryDifferentialEquationService):
    def __init__(self, main_figure: Figure):
        super().__init__(main_figure)

    def compute_solution(self, metadata: OrdinaryDifferentialEquationMetadata) -> np.ndarray:
        start_time = timeit.default_timer()
        N = metadata.samples
        dt = metadata.time / (N - 1)
        initial_value, derivative = metadata.initial_derivatives
        source: Callable[[float, float, float], float] = lambda t, x, y: eval(metadata.source)
        solution = np.zeros(N)
        solution[0] = initial_value
        for i in range(1, N):
            derivative_delta = source((i - 1) * dt, solution[i - 1], derivative) * dt
            derivative = derivative + derivative_delta
            solution[i] = solution[i - 1] + derivative * dt
        total_time = timeit.default_timer() - start_time
        print(f"computing second order ode solution took {total_time} seconds")
        return solution

    def validate_metadata(self, metadata: OrdinaryDifferentialEquationMetadata):
        if metadata.samples <= 1 or metadata.time == 0:
            raise Exception("invalid second order ode metadata")
