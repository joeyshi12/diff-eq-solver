import os
import abc
import xlsxwriter
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from exception.BoundaryTypeException import BoundaryTypeException


class PDE:
    u: np.ndarray
    x_range: np.ndarray
    t_range: np.ndarray

    # boundary_type is an int in [1, 4]
    # Interp. - 1: u(0,t)   = p(t),     u(L,t)   = q(t)
    #         - 2: u_x(0,t) = p(t),     u_x(L,t) = q(t)
    #         - 3: u(0,t)   = p(t),     u_x(L,t) = q(t)
    #         - 4: u_x(0,t) = p(t),     u(L,t)   = q(t)

    def __init__(self, boundary_type, p, q):
        self.boundary_type = boundary_type
        self.p = p
        self.q = q

    def solve(self, L, n, t, m):
        dx = L / n
        dt = t / m
        self.x_range = np.arange(n + 1) * dx
        self.t_range = np.arange(m + 1) * dt
        k = self.k_val(dx, dt)
        if self.boundary_type == 1:
            self.solve_dirichlet(dx, dt, n, m, k)
        elif self.boundary_type == 2:
            self.solve_neumann(dx, dt, n, m, k)
        elif self.boundary_type == 3:
            self.solve_mixed_1(dx, dt, n, m, k)
        elif self.boundary_type == 4:
            self.solve_mixed_2(dx, dt, n, m, k)
        else:
            raise BoundaryTypeException

    def write_solution(self):
        m = self.u.shape[0] - 1
        n = self.u.shape[1] - 1
        workbook = xlsxwriter.Workbook('excel_data/PDE.xlsx')
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 1, "x →")
        for i in range(n + 1):
            worksheet.write(0, 2 + i, self.x_range[i])

        worksheet.write(1, 0, "t ↓")
        for j in range(m + 1):
            worksheet.write(2 + j, 0, self.t_range[j])

        for j in range(m + 1):
            for i in range(n + 1):
                worksheet.write(j + 2, i + 2, self.u[j, i])
        workbook.close()

    def plot_solution(self):
        x_mesh, t_mesh = np.meshgrid(self.x_range, self.t_range)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(x_mesh, t_mesh, self.u, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        fig.colorbar(surf, shrink=0.5, aspect=5)

    def animate_solution(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.x_range[-1])
        ax.set_ylim(np.min(self.u), np.max(self.u))
        line, = ax.plot(0, 0)

        def animation_frame(i):
            line.set_xdata(self.x_range)
            line.set_ydata(self.u[i, np.arange(self.x_range.size)])
            return line,

        FuncAnimation(fig, func=animation_frame, frames=np.arange(0, self.u.shape[0], 1))
        plt.show()

    @abc.abstractmethod
    def solve_dirichlet(self, dx, dt, n, m, k):
        pass

    @abc.abstractmethod
    def solve_neumann(self, dx, dt, n, m, k):
        pass

    @abc.abstractmethod
    def solve_mixed_1(self, dx, dt, n, m, k):
        pass

    @abc.abstractmethod
    def solve_mixed_2(self, dx, dt, n, m, k):
        pass

    @abc.abstractmethod
    def k_val(self, dx, dt) -> float:
        pass
