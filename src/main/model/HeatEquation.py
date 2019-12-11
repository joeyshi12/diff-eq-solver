import xlsxwriter
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from src.main.exception.BoundaryTypeException import BoundaryTypeException
from src.main.model.PDE import PDE


class HeatEquation(PDE):
    alpha: float

    def __init__(self, alpha: float, boundary_type: int, p, q, f):
        self.alpha = alpha
        super().__init__(boundary_type)
        self.p = p  # boundary condition 1
        self.q = q  # boundary condition 2
        self.f = f  # initial condition

    def integrate_dirichlet(self, dt: float, dx: float, m: int, n: int) -> np.array:
        k = self.alpha * dt / dx ** 2
        u = []
        # initial condition
        u_0 = [self.f(i * dx) for i in range(1, n)]
        # initial boundary conditions
        u_0 = [self.p(0)] + u_0 + [self.q(0)]
        u.append(u_0)
        for j in range(1, m + 1):
            # nodal values
            u_j = [self.node_val(u, k, i, j) for i in range(1, n)]
            # boundary values
            u_j = [self.p(j * dt)] + u_j + [self.q(j * dt)]
            u.append(u_j)
        return np.array(u)

    def integrate_neumann(self, dt: float, dx: float, m: int, n: int) -> np.array:
        k = self.alpha * dt / dx ** 2
        u = []
        # initial condition
        u_0 = [self.f(i * dx) for i in range(n + 1)]
        # initial boundary conditions
        u_0 = [u_0[0] - 2 * self.p(0) * dx] + u_0 + [u_0[-1] + 2 * self.q(0) * dx]
        u.append(u_0)
        for j in range(1, m + 1):
            # nodal values
            u_j = [self.node_val(u, k, i, j) for i in range(1, n + 2)]
            # boundary values
            u_j = [u_j[1] - 2 * self.p(j * dt)] + u_j + [u_j[-2] + 2 * self.q(j * dt)]
            u.append(u_j)
        u = np.delete(u, 0, 1)
        u = np.delete(u, n + 1, 1)
        return u

    def integrate_mixed_1(self, dt: float, dx: float, m: int, n: int) -> np.array:
        k = self.alpha * dt / dx ** 2
        u = []
        # initial condition
        u_0 = [self.f(i * dx) for i in range(1, n + 1)]
        # initial boundary conditions
        u_0 = [self.p(0)] + u_0 + [u_0[-2] + 2 * self.q(0) * dx]
        u.append(u_0)
        for j in range(1, m + 1):
            # nodal values
            u_j = [self.node_val(u, k, i, j) for i in range(1, n + 1)]
            # boundary values
            u_j = [self.p(j * dt)] + u_j + [u_j[n - 1] + 2 * self.q(j * dt)]
            u.append(u_j)
        u = np.delete(u, n + 1, 1)
        return u

    def integrate_mixed_2(self, dt: float, dx: float, m: int, n: int) -> np.array:
        k = self.alpha * dt / dx ** 2
        u = []
        # initial condition
        u_0 = [self.f(i * dx) for i in range(n)]
        # initial boundary condition
        u_0 = [u_0[1] - 2 * self.p(0) * dx] + u_0 + [self.q(0)]
        u.append(u_0)
        for j in range(1, m + 1):
            # nodal values
            u_j = [self.node_val(u, k, i, j) for i in range(1, n + 1)]
            # boundary values
            u_j = [u_j[1] - 2 * self.p(j * dt)] + u_j + [self.q(n)]
            u.append(u_j)
        u = np.delete(u, 0, 1)
        return u

    @staticmethod
    def node_val(u, k, i, j):
        return u[j - 1][i] + k * (u[j - 1][i + 1] - 2 * u[j - 1][i] + u[j - 1][i - 1])

    def get_stable_m(self, L, n, t):
        m = np.ceil(2 * self.alpha * t * n ** 2 / (L ** 2))
        return int(m)
