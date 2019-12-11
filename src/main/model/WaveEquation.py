import numpy as np

from src.main.model.PDE import PDE


class WaveEquation(PDE):
    c: float

    def __init__(self, c: float, boundary_type: int, p, q, f, g):
        self.c = c
        super().__init__(boundary_type)
        self.p = p  # left boundary
        self.q = q  # right boundary
        self.f = f  # initial values
        self.g = g  # initial derivatives

    def integrate_dirichlet(self, dx: float, dt: float, n: int, m: int, k) -> np.array:
        u = []
        u_0 = [self.f(i * dx) for i in range(1, n)] # initial values
        u_0 = [self.p(0)] + u_0 + [self.q(0)]       # initial boundary conditions
        u.append(u_0)

        u_1 = [(k ** 2 * u_0[i + 1] + 2 * (1 - k ** 2) * u_0[i] + k ** 2 * u_0[i - 1]) / 2 + dt * self.g(i * dx)
               for i in range(1, n)]                # next values
        u_1 = [self.p(dt)] + u_1 + [self.q(dt)]     # next boundary conditions
        u.append(u_1)

        for j in range(2, m + 1):
            u_j = [self.node_val(u, k, i, j) for i in range(1, n)]  # nodal values
            u_j = [self.p(j * dt)] + u_j + [self.q(j * dt)]         # boundary values
            u.append(u_j)
        return np.array(u)

    def integrate_neumann(self, dx: float, dt: float, n: int, m: int, k: float) -> np.array:
        return np.array([])

    def integrate_mixed_1(self, dx: float, dt: float, n: int, m: int, k: float) -> np.array:
        return np.array([])

    def integrate_mixed_2(self, dx: float, dt: float, n: int, m: int, k: float) -> np.array:
        return np.array([])

    def get_k(self, dx: float, dt: float) -> float:
        return self.c * dt / dx

    @staticmethod
    def node_val(u: np.array, k: float, i: int, j: int) -> float:
        return k ** 2 * u[j - 1][i + 1] + 2 * (1 - k ** 2) * u[j - 1][i] + k ** 2 * u[j - 1][i - 1] - u[j - 2][i]

    def get_stable_m(self, L: float, n: int, t: float) -> int:
        m = np.ceil(self.c * t * n / L)
        return int(m)