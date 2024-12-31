import timeit
from typing import Callable
import numpy as np

from diffeq_solver_tk.diffeq import OrdinaryDifferentialEquationMetadata, \
    HeatEquationMetadata, WaveEquationMetadata, BoundaryType


def solve_first_order_ode(metadata: OrdinaryDifferentialEquationMetadata) -> np.ndarray:
    if metadata.samples <= 1 or metadata.time == 0:
        raise Exception("invalid first order ode metadata")

    start_time = timeit.default_timer()
    N = metadata.samples
    dt = metadata.time / (N - 1)
    source: Callable[[float, float], float] = lambda t, x: eval(metadata.source)
    solution = np.zeros(N)
    solution[0] = metadata.initial_derivatives[0]
    for i in range(1, N):
        solution[i] = solution[i - 1] + source(i * dt, solution[i - 1]) * dt
    total_time = timeit.default_timer() - start_time
    print(f"computing first order ode solution took {total_time} seconds")
    return solution


def solve_second_order_ode(metadata: OrdinaryDifferentialEquationMetadata) -> np.ndarray:
    if metadata.samples <= 1 or metadata.time == 0:
        raise Exception("invalid second order ode metadata")

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


def solve_heat_equation(metadata: HeatEquationMetadata) -> np.ndarray:
    if metadata.samples <= 1 or metadata.length == 0 or metadata.time == 0:
        raise Exception("invalid heat equation metadata")

    start_time = timeit.default_timer()
    initial_values: Callable[[float], float] = lambda x: eval(metadata.initial_values)
    source: Callable[[float, float], float] = lambda t, x: eval(metadata.source)
    N = metadata.samples
    dx = metadata.length / (N - 1)
    K = 2 * int(2 * metadata.alpha * metadata.time / dx ** 2) + 1
    dt = metadata.time / (K - 1)
    D = create_heat_equation_time_step_matrix(metadata.alpha * dt / dx ** 2, N)
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


def solve_wave_equation(metadata: WaveEquationMetadata) -> np.ndarray:
    if metadata.samples <= 1 or metadata.length == 0 or metadata.time == 0:
        raise Exception("invalid wave equation metadata")

    start_time = timeit.default_timer()
    initial_values: Callable[[float], float] = lambda x: eval(metadata.initial_values)
    initial_derivatives: Callable[[float], float] = lambda x: eval(metadata.initial_derivatives)
    source: Callable[[float, float], float] = lambda t, x: eval(metadata.source)
    N = metadata.samples
    dx = metadata.length / (N - 1)
    K = 2 * int(metadata.wave_speed * metadata.time / dx) + 1
    dt = metadata.time / (K - 1)
    D = create_wave_equation_time_step_matrix((metadata.wave_speed * dt / dx) ** 2, N)
    left_values: Callable[[float], float] = lambda t: eval(metadata.boundary_conditions.left.values)
    right_values: Callable[[float], float] = lambda t: eval(metadata.boundary_conditions.right.values)
    is_left_dirichlet = metadata.boundary_conditions.left.type == BoundaryType.DIRICHLET
    is_right_dirichlet = metadata.boundary_conditions.right.type == BoundaryType.DIRICHLET

    # Initialize solution array
    solution = np.zeros((K, N))
    solution[0] = initial_values(np.arange(N) * dx)
    solution[1, 1:N - 1] = (1 / 2) * D @ solution[0]
    solution[1, 1:N - 1] += dt ** 2 * initial_derivatives(np.arange(1, N - 1) * dx)
    solution[1, 1:N - 1] += (dt ** 2 / 2) * source(dt, np.arange(1, N - 1) * dx)
    solution[1, 0] = left_values(dt) if is_left_dirichlet else solution[1, 1] - left_values(dt) * dx
    solution[1, -1] = right_values(dt) if is_right_dirichlet else solution[1, -2] + right_values(dt) * dx
    for k in range(2, K):
        T = k * dt
        solution[k, 1:N - 1] = D @ solution[k - 1] - solution[k - 2, 1:N - 1]
        solution[k, 1:N - 1] += dt ** 2 * source(T, np.arange(1, N - 1) * dx)
        solution[k, 0] = left_values(T) if is_left_dirichlet else solution[k, 1] - left_values(T) * dx
        solution[k, -1] = right_values(T) if is_right_dirichlet else solution[k, -2] + right_values(T) * dx

    total_time = timeit.default_timer() - start_time
    print(f"computing wave equation solution took {total_time} seconds")
    return solution


def create_heat_equation_time_step_matrix(r: float, N: int) -> np.ndarray:
    D = np.zeros((N - 2, N))
    for i in range(N - 2):
        D[i, i] = r
        D[i, i + 1] = 1 - 2 * r
        D[i, i + 2] = r
    return D


def create_wave_equation_time_step_matrix(r: float, N: int) -> np.ndarray:
    D = np.zeros((N - 2, N))
    for i in range(N - 2):
        D[i, i] = r
        D[i, i + 1] = 2 * (1 - r)
        D[i, i + 2] = r
    return D
