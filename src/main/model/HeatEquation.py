import xlsxwriter
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


class HeatEquation:
    alpha: float
    boundary_type: int

    # boundary_condition is one-of
    # 0, 1 ,2 ,3
    # Interp. - 0: u(0,t)   = p(t),     u(L,t)   = q(t)
    #         - 1: u_x(0,t) = p(t),     u_x(L,t) = q(t)
    #         - 2: u(0,t)   = p(t),     u_x(L,t) = q(t)
    #         - 3: u_x(0,t) = p(t),     u(L,t)   = q(t)

    def __init__(self, alpha: float, boundary_type: int, p, q, f):
        self.alpha = alpha
        self.boundary_type = boundary_type
        self.p = p  # boundary condition 1
        self.q = q  # boundary condition 2
        self.f = f  # initial condition

    def integrate(self, L: float, n: int, t: float, m: int) -> np.ndarray:
        dx = L / n
        dt = t / m
        k = self.alpha * dt / dx ** 2

        if self.boundary_type == 0:
            return self.integrate_dirichlet(dt, dx, k, m, n)
        elif self.boundary_type == 1:
            return self.integrate_neumann(dt, dx, k, m, n)
        elif self.boundary_type == 2:
            return self.integrate_mixed_1(dt, dx, k, m, n)
        elif self.boundary_type == 3:
            return self.integrate_mixed_2(dt, dx, k, m, n)

    def integrate_dirichlet(self, dt: float, dx: float, k: float, m: int, n: int) -> np.array:
        u = []
        # initial condition
        u_0 = [self.f(i * dx) for i in range(1, n)]
        # initial boundary conditions
        u_0 = [self.p(0)] + u_0 + [self.q(0)]
        u.append(u_0)
        for j in range(1, m + 1):
            # nodal values
            u_j = [u[j - 1][i] + k * (u[j - 1][i + 1] - 2 * u[j - 1][i] + u[j - 1][i - 1]) for i in range(1, n)]
            # boundary values
            u_j = [self.p(j * dt)] + u_j + [self.q(j * dt)]
            u.append(u_j)
        return np.array(u)

    def integrate_neumann(self, dt: float, dx: float, k: float, m: int, n: int) -> np.array:
        u = []
        # initial condition
        u_0 = [self.f(i * dx) for i in range(n + 1)]
        # initial boundary conditions
        u_0 = [u_0[0] - 2 * self.p(0) * dx] + u_0 + [u_0[-1] - 2 * self.q(0) * dx]
        u.append(u_0)
        print(u_0)
        for j in range(1, m + 1):
            # nodal values
            u_j = [u[j - 1][i] + k * (u[j - 1][i + 1] - 2 * u[j - 1][i] + u[j - 1][i - 1]) for i in range(1, n + 2)]
            # boundary values
            u_j = [u_j[1] - 2 * self.p(j * dt)] + u_j + [u_j[-2] - 2 * self.q(j * dt)]
            u.append(u_j)
        u = np.delete(u, 0, 1)
        u = np.delete(u, n + 1, 1)
        return u

    def integrate_mixed_1(self, dt: float, dx: float, k: float, m: int, n: int) -> np.array:
        u = []
        # initial condition
        u_0 = [self.f(i * dx) for i in range(1, n + 1)]
        # initial boundary conditions
        u_0 = [self.p(0)] + u_0 + [u_0[-2] - 2 * self.q(0) * dx]
        u.append(u_0)
        for j in range(1, m + 1):
            # nodal values
            u_j = [u[j - 1][i] + k * (u[j - 1][i + 1] - 2 * u[j - 1][i] + u[j - 1][i - 1]) for i in range(1, n + 1)]
            # boundary values
            u_j = [self.p(j * dt)] + u_j + [u_j[n - 1] - 2 * self.q(j * dt)]
            u.append(u_j)
        u = np.delete(u, n + 1, 1)
        return u

    def integrate_mixed_2(self, dt: float, dx: float, k: float, m: int, n: int) -> np.array:
        u = []
        # initial condition
        u_0 = [self.f(i * dx) for i in range(n)]
        # initial boundary condition
        u_0 = [u_0[1] - 2 * self.p(0) * dx] + u_0 + [self.q(0)]
        u.append(u_0)
        for j in range(1, m + 1):
            # nodal values
            u_j = [u[j - 1][i] + k * (u[j - 1][i + 1] - 2 * u[j - 1][i] + u[j - 1][i - 1]) for i in range(1, n + 1)]
            # boundary values
            u_j = [u_j[1] - 2 * self.p(j * dt)] + u_j + [self.q(n)]
            u.append(u_j)
        u = np.delete(u, 0, 1)
        return u

    def write_solution(self, L: float, n: int, t: float):
        dx = L / n
        m = np.ceil(2 * self.alpha * t / (dx ** 2))
        m = int(m)

        # Data
        x_range = np.linspace(0, L, n + 1)
        t_range = np.linspace(0, t, m + 1)
        u = self.integrate(L, n, t, m)

        workbook = xlsxwriter.Workbook(r'C:\Users\j\Desktop\PycharmProjects\DifferentialEquationSolver\src\data'
                                       r'\HeatEquation.xlsx')
        worksheet = workbook.add_worksheet()

        # x labels
        worksheet.write(0, 1, "x ->")
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

    def plot_solution(self, L: float, n: int, t: float):
        dx = L / n
        m = np.ceil(2 * self.alpha * t / (dx ** 2))
        m = int(m)

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

        # Customize the z axis.
        ax.set_zlim(-1.01, 1.01)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)