from abc import abstractmethod, ABC
from typing import Callable

import xlsxwriter
import numpy as np
from matplotlib import animation, cm
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D

from src.differential_equation_metadata import DifferentialEquationMetadata, BoundedEquationMetadata, BoundaryType


class DifferentialEquation:
    metadata: DifferentialEquationMetadata
    solution: np.ndarray

    def __init__(self, metadata: DifferentialEquationMetadata):
        self.validate_metadata(metadata)
        self.metadata = metadata

    def get_solution(self):
        return self.solution

    @abstractmethod
    def compute_solution(self) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def initialize_figure(self, figure: Figure):
        raise NotImplementedError

    @abstractmethod
    def save_solution(self, path):
        raise NotImplementedError

    @abstractmethod
    def validate_metadata(self, metadata: DifferentialEquationMetadata):
        raise NotImplementedError


class ODE(DifferentialEquation, ABC):
    dt: float

    def initialize_figure(self, figure: Figure):
        ax = figure.add_subplot()
        N = self.solution.size
        ax.plot(np.arange(N) * self.dt, self.solution)
        ax.set_xlabel("t [time]")
        ax.set_ylabel("x(t)")
        ax.plot()
        ax.set_title("Solution: x(t)")

    def save_solution(self, path):
        N = self.solution.size
        table = np.column_stack((np.arange(N) * self.dt, self.solution))
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, 't')
        worksheet.write(0, 1, 'x')
        row = 1
        for t_val, x_val in table:
            worksheet.write(row, 0, t_val)
            worksheet.write(row, 1, x_val)
            row += 1
        workbook.close()


class BoundedEquation(DifferentialEquation, ABC):
    metadata: BoundedEquationMetadata
    left_values: Callable[[float], float]  # (t: float) -> float
    right_values: Callable[[float], float]  # (t: float) -> float
    dt: float
    dx: float

    def __init__(self, metadata: DifferentialEquationMetadata):
        super().__init__(metadata)
        self.left_values = lambda t: eval(self.metadata.boundary_conditions.left.values)
        self.right_values = lambda t: eval(self.metadata.boundary_conditions.right.values)

    def initialize_figure(self, figure):
        K, N = self.solution.shape
        x, t = np.meshgrid(np.arange(N) * self.dx, np.arange(K) * self.dt)
        ax = figure.gca(projection='3d')
        ax.set_xlabel('x [length]')
        ax.set_ylabel('t [time]')
        ax.set_zlabel('u(x, t)')
        surf = ax.plot_surface(x, t, self.solution, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        figure.colorbar(surf, shrink=0.5, aspect=5)

    def get_animation(self, fig: Figure):
        K, N = self.solution.shape
        ax = fig.add_subplot()
        Axes.set_xlim(ax, left=0, right=(N - 1) * self.dx)
        Axes.set_ylim(ax, bottom=np.min(self.solution), top=np.max(self.solution))
        ax.set_xlabel("x [length]")
        ax.set_ylabel("u(x, t)")
        ax.set_title("Solution: u(x, t)")
        line, = ax.plot(np.arange(N) * self.dx, self.solution[0], "-o", markersize=4)
        time_text = ax.text(0.82, 0.92, '', transform=ax.transAxes)

        def update_plot(k):
            line.set_ydata(self.solution[k])
            time_text.set_text("t = %.3f" % (k * self.dt))
            return line, time_text

        anim = animation.FuncAnimation(fig, update_plot, frames=K, blit=True, interval=20)
        return anim

    def save_solution(self, path):
        K, N = self.solution.shape
        t = np.arange(K) * self.dt
        x = np.arange(N) * self.dx
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 1, "x →")
        for i in range(N):
            worksheet.write(0, 2 + i, x[i])
        worksheet.write(1, 0, "t ↓")
        for k in range(K):
            worksheet.write(2 + k, 0, t[k])
        for k in range(K):
            for i in range(N):
                worksheet.write(k + 2, i + 2, self.solution[k, i])
        workbook.close()

    def fill_boundary_values(self, k):
        if self.metadata.boundary_conditions.left.type == BoundaryType.DIRICHLET:
            self.solution[k, 0] = self.left_values(k * self.dt)
        else:
            self.solution[k, 0] = self.solution[k, 1] - self.left_values(k * self.dt) * self.dx
        if self.metadata.boundary_conditions.right.type == BoundaryType.DIRICHLET:
            self.solution[k, -1] = self.right_values(k * self.dt)
        else:
            self.solution[k, -1] = self.solution[k, -2] + self.right_values(k * self.dt) * self.dx
