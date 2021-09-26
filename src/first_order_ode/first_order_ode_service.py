from typing import Callable

import numpy as np
from matplotlib.figure import Figure

from src.differential_equation_metadata import OrdinaryDifferentialEquationMetadata
from src.differential_equation_service import OrdinaryDifferentialEquationService


class FirstOrderODEService(OrdinaryDifferentialEquationService):
    def __init__(self, main_figure: Figure):
        super().__init__(main_figure, "FirstOrderODE")

    def compute_solution(self, metadata: OrdinaryDifferentialEquationMetadata) -> np.ndarray:
        N = metadata.samples
        dt = metadata.time / (N - 1)
        source: Callable[[float, float], float] = lambda t, x: eval(metadata.source)
        solution = np.zeros(N)
        solution[0] = metadata.initial_derivatives[0]
        for i in range(1, N):
            solution[i] = solution[i - 1] + source(i * dt, solution[i - 1]) * dt
        return solution

    def validate_metadata(self, metadata: OrdinaryDifferentialEquationMetadata):
        if metadata.samples <= 1 or metadata.time == 0:
            raise Exception("invalid first order ode metadata")
