import abc

import xlsxwriter
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm

from exception.BoundaryTypeException import BoundaryTypeException


class PDE:
    boundary_type: int

    # boundary_type is an int in [0, 3]
    # Interp. - 0: u(0,t)   = p(t),     u(L,t)   = q(t)
    #         - 1: u_x(0,t) = p(t),     u_x(L,t) = q(t)
    #         - 2: u(0,t)   = p(t),     u_x(L,t) = q(t)
    #         - 3: u_x(0,t) = p(t),     u(L,t)   = q(t)

    def __init__(self, boundary_type, p, q):
        self.boundary_type = boundary_type
        self.p = p
        self.q = q

    def integrate(self, L: float, n: int, t: float, m: int) -> np.ndarray:
        dx = L / n
        dt = t / m
        k = self.calc_k(dx, dt)
        if self.boundary_type == 0:
            return self.integrate_dirichlet(dx, dt, n, m, k)
        elif self.boundary_type == 1:
            return self.integrate_neumann(dx, dt, n, m, k)
        elif self.boundary_type == 2:
            return self.integrate_mixed_1(dx, dt, n, m, k)
        elif self.boundary_type == 3:
            return self.integrate_mixed_2(dx, dt, n, m, k)
        else:
            raise BoundaryTypeException

    def add_layer_dirichlet(self, dt, j, k, n, u):
        u_j = [self.node_val(u, k, i, j) for i in range(1, n)]                  # nodal values
        u_j = [self.p(j * dt)] + u_j + [self.q(j * dt)]                         # boundary values
        u.append(u_j)

    def add_layer_neumann(self, dt, dx, j, k, n, u):
        u_j = [self.node_val(u, k, i, j) for i in range(1, n + 2)]                              # nodal values
        u_j = [u_j[1] - 2 * self.p(j * dt) * dx] + u_j + [u_j[-2] + 2 * self.q(j * dt) * dx]    # boundary values
        u.append(u_j)

    def add_layer_mixed_1(self, dt, dx, j, k, n, u):
        u_j = [self.node_val(u, k, i, j) for i in range(1, n + 1)]              # nodal values
        u_j = [self.p(j * dt)] + u_j + [u_j[n - 1] + 2 * self.q(j * dt) * dx]   # boundary values
        u.append(u_j)

    def add_layer_mixed_2(self, dt, dx, j, k, n, u):
        u_j = [self.node_val(u, k, i, j) for i in range(1, n + 1)]              # nodal values
        u_j = [u_j[1] - 2 * self.p(j * dt) * dx] + u_j + [self.q(j * dt)]       # boundary values
        u.append(u_j)

    def write_solution(self, L: float, n: int, t: float, m: int):
        # Data
        x_range = np.linspace(0, L, n + 1)
        t_range = np.linspace(0, t, m + 1)
        u = self.integrate(L, n, t, m)
        workbook = xlsxwriter.Workbook('excel_data/PDE.xlsx')
        worksheet = workbook.add_worksheet()

        # x labels
        worksheet.write(0, 1, "x →")
        for i in range(n + 1):
            worksheet.write(0, 2 + i, x_range[i])

        # t labels
        worksheet.write(1, 0, "t ↓")
        for j in range(m + 1):
            worksheet.write(2 + j, 0, t_range[j])

        # u values
        for j in range(m + 1):
            for i in range(n + 1):
                worksheet.write(j+2, i+2, u[j][i])
        workbook.close()

    def plot_solution(self, L: float, n: int, t: float, m: int):
        # Data
        x_range = np.linspace(0, L, n + 1)
        t_range = np.linspace(0, t, m + 1)
        x_range, t_range = np.meshgrid(x_range, t_range)
        u = self.integrate(L, n, t, m)

        # Plot
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(x_range, t_range, u, cmap=cm.coolwarm, linewidth=0, antialiased=False)

        # Colour Bar
        fig.colorbar(surf, shrink=0.5, aspect=5)

    @abc.abstractmethod
    def integrate_dirichlet(self, dx: float, dt: float, n: int, m: int, k: float) -> np.array:
        pass

    @abc.abstractmethod
    def integrate_neumann(self, dx: float, dt: float, n: int, m: int, k: float) -> np.array:
        pass

    @abc.abstractmethod
    def integrate_mixed_1(self, dx: float, dt: float, n: int, m: int, k: float) -> np.array:
        pass

    @abc.abstractmethod
    def integrate_mixed_2(self, dx: float, dt: float, n: int, m: int, k: float) -> np.array:
        pass

    @abc.abstractmethod
    def node_val(self, u: np.array, k: float, i: int, j: int) -> float:
        pass

    @abc.abstractmethod
    def calc_k(self, dx: float, dt: float) -> float:
        pass
