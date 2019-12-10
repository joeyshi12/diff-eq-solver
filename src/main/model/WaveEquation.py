import numpy as np
import matplotlib.pyplot as plt


class WaveEquation:
    c: float
    boundary_type: int

    # boundary_type is one-of
    # 0, 1 ,2 ,3
    # Interp. - 0: u(0,t)   = p(t),     u(L,t)   = q(t)
    #         - 1: u_x(0,t) = p(t),     u_x(L,t) = q(t)
    #         - 2: u(0,t)   = p(t),     u_x(L,t) = q(t)
    #         - 3: u_x(0,t) = p(t),     u(L,t)   = q(t)

    def __init__(self, c: float, boundary_type: int, p, q, f, g):
        self.c = c
        self.boundary_type = boundary_type
        self.p = p  # left boundary
        self.q = q  # right boundary
        self.f = f  # initial values
        self.g = g  # initial derivatives

    def integrate(L: float, n: int, t: float, m: int) -> np.ndarray:
        return np.array([]) # stub

    def write_solution(self, L: float, n: int, t: float):
        return # stub

    def plot_solution(self, L: float, n: int, t: float):
        return # stub
