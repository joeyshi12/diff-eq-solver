import abc

import xlsxwriter
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from src.main.exception.BoundaryTypeException import BoundaryTypeException


class PDE:
    boundary_type: int

    # boundary_type is one-of
    # 0, 1 ,2 ,3
    # Interp. - 0: u(0,t)   = p(t),     u(L,t)   = q(t)
    #         - 1: u_x(0,t) = p(t),     u_x(L,t) = q(t)
    #         - 2: u(0,t)   = p(t),     u_x(L,t) = q(t)
    #         - 3: u_x(0,t) = p(t),     u(L,t)   = q(t)

    def __init__(self, boundary_type):
        self.boundary_type = boundary_type

    def integrate(self, L: float, n: int, t: float, m: int) -> np.ndarray:
        dx = L / n
        dt = t / m
        if self.boundary_type == 0:
            return self.integrate_dirichlet(dt, dx, m, n)
        elif self.boundary_type == 1:
            return self.integrate_neumann(dt, dx, m, n)
        elif self.boundary_type == 2:
            return self.integrate_mixed_1(dt, dx, m, n)
        elif self.boundary_type == 3:
            return self.integrate_mixed_2(dt, dx, m, n)
        else:
            raise BoundaryTypeException

    @abc.abstractmethod
    def integrate_dirichlet(self, dt, dx, m, n):
        pass

    @abc.abstractmethod
    def integrate_neumann(self, dt, dx, m, n):
        pass

    @abc.abstractmethod
    def integrate_mixed_1(self, dt, dx, m, n):
        pass

    @abc.abstractmethod
    def integrate_mixed_2(self, dt, dx, m, n):
        pass

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
        i, j = 2, 2
        for row in u:
            for element in row:
                worksheet.write(j, i, element)
                i += 1
            j += 1
            i = 2
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
        surf = ax.plot_surface(x_range, t_range, u, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)

        # Colour Bar
        fig.colorbar(surf, shrink=0.5, aspect=5)