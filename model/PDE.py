import os
import abc
import xlsxwriter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d
from matplotlib import cm
from exception.BoundaryTypeException import BoundaryTypeException


class PDE:
    u: np.ndarray
    x_data: np.ndarray
    t_data: np.ndarray
    # boundary_type is an int in [1, 4]
    # Interp. - 1: u(0,t)   = p(t),     u(L,t)   = q(t)
    #         - 2: u_x(0,t) = p(t),     u_x(L,t) = q(t)
    #         - 3: u(0,t)   = p(t),     u_x(L,t) = q(t)
    #         - 4: u_x(0,t) = p(t),     u(L,t)   = q(t)

    def __init__(self, boundary_type, p, q, filename):
        self.boundary_type = boundary_type
        self.p = p
        self.q = q
        self.filename = filename

    def solve(self, L, n, t, m):
        """computes solution into u as an (m+1)x(n+1) matrix"""
        dx = L / n
        dt = t / m
        self.x_data = np.arange(n + 1) * dx
        self.t_data = np.arange(m + 1) * dt
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
        """writes the values of u into a table inside of an xlsx file named filename"""
        m = self.u.shape[0] - 1
        n = self.u.shape[1] - 1
        dirname = os.path.dirname(__file__)
        workbook = xlsxwriter.Workbook(os.path.join(dirname, '..', 'output', self.filename))
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 1, "x →")
        for i in range(n + 1):
            worksheet.write(0, 2 + i, self.x_data[i])

        worksheet.write(1, 0, "t ↓")
        for j in range(m + 1):
            worksheet.write(2 + j, 0, self.t_data[j])

        for j in range(m + 1):
            for i in range(n + 1):
                worksheet.write(j + 2, i + 2, self.u[j, i])
        workbook.close()

    def plot_solution(self):
        """plots u onto a 3d figure as a function of (x, t)"""
        x_mesh, t_mesh = np.meshgrid(self.x_data, self.t_data)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(x_mesh, t_mesh, self.u, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.title("Solution Plot")
        plt.show()

    def animate_solution(self):
        """plots animation where the jth frame is a plot of (x_range, u[j, x_range])"""
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.x_data[-1])
        ax.set_ylim(np.min(self.u), np.max(self.u))
        line, = ax.plot(0, 0)

        def animation_frame(i):
            line.set_xdata(self.x_data)
            line.set_ydata(self.u[i, np.arange(self.x_data.size)])
            return line,

        animation = FuncAnimation(fig, func=animation_frame, frames=np.arange(0, self.u.shape[0], 1),
                                  interval=self.t_data[-1] / self.u.shape[0])
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
