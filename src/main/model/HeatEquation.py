from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

class HeatEquation:
    alpha: float
    boundary_condition: int
    # boundary_condition is one-of
    # 0, 1 ,2 ,3
    # Interp. - 0: Dirichlet BC
    #         - 1: Neumann BC
    #         - 2: Mixed 1 BC
    #         - 3: Mixed 2 BC

    def __init__(self, alpha: float, boundary_condition: int, initial_condition):
        self.alpha = alpha
        self.boundary_condition = boundary_condition
        self.initial_condition = initial_condition


    def integrate(self, L, N, t):
        dx = L/N
        M = np.ceil(2*t/dx**2)
        M = int(M)
        dt = t/M
        u = []
        if self.boundary_condition == 0:
            u_i = []
            for n in range(N+1):
                u_i.append(self.initial_condition(n*dx))
            u.append(u_i)
            for m in range(1,M):
                u_i = []
                for n in range(N+1):
                    if n == 0 or n == N:
                        u_i.append(0)
                    else:
                        u_i.append(u[m-1][n] + (dt/dx**2)*(u[m-1][n+1] - 2*u[m-1][n] + u[m-1][n-1]))
                u.append(u_i)
        return u

    def plot_solution(self, L, N, T):
        dx = L / N
        M = np.ceil(2 * T / dx ** 2)
        M = int(M)

        # Data
        x = np.linspace(0, L, N + 1)
        t = np.linspace(0, T, M)
        x, t = np.meshgrid(x, t)
        u = self.integrate(L, N, T)
        u = np.array(u)

        # Plot
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(x, t, u, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)

        # Customize the z axis.
        ax.set_zlim(-1.01, 1.01)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)

