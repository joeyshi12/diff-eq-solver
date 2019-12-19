import numpy as np

from model.PDE import PDE


class HeatEquation(PDE):
    alpha: float

    def __init__(self, alpha: float, boundary_type: int, p, q, f):
        self.alpha = alpha
        super().__init__(boundary_type)
        self.p = p  # boundary condition 1
        self.q = q  # boundary condition 2
        self.f = f  # initial values

    def integrate_dirichlet(self, dx: float, dt: float, n: int, m: int, k) -> np.array:
        u = []
        u_0 = [self.f(i * dx) for i in range(n + 1)]                 # initial condition
        u.append(u_0)
        for j in range(1, m + 1):
            u_j = [self.node_val(u, k, i, j) for i in range(1, n)]  # nodal values
            u_j = [self.p(j * dt)] + u_j + [self.q(j * dt)]         # boundary values
            u.append(u_j)
        return np.array(u)

    def integrate_neumann(self, dx: float, dt: float, n: int, m: int, k) -> np.array:
        u = []
        u_0 = [self.f(i * dx) for i in range(n + 1)]                                    # initial values
        u_0 = [u_0[1] - 2 * self.p(0) * dx] + u_0 + [u_0[-2] + 2 * self.q(0) * dx]      # initial boundary values
        u.append(u_0)
        for j in range(1, m + 1):
            u_j = [self.node_val(u, k, i, j) for i in range(1, n + 2)]                  # nodal values
            u_j = [u_j[1] - 2 * self.p(j * dt) * dx] + u_j + [u_j[-2] + 2 * self.q(j * dt) * dx]  # boundary values
            u.append(u_j)
        u = np.delete(u, 0, 1)
        u = np.delete(u, n + 1, 1)
        return u

    def integrate_mixed_1(self, dx: float, dt: float, n: int, m: int, k) -> np.array:
        u = []
        u_0 = [self.f(i * dx) for i in range(n + 1)]                         # initial values
        u_0 = u_0 + [u_0[-2] + 2 * self.q(0) * dx]                # initial boundary values
        u.append(u_0)
        for j in range(1, m + 1):
            u_j = [self.node_val(u, k, i, j) for i in range(1, n + 1)]          # nodal values
            u_j = [self.p(j * dt)] + u_j + [u_j[n - 1] + 2 * self.q(j * dt) * dx]    # boundary values
            u.append(u_j)
        u = np.delete(u, n + 1, 1)
        return u

    def integrate_mixed_2(self, dx: float, dt: float, n: int, m: int, k) -> np.array:
        u = []
        u_0 = [self.f(i * dx) for i in range(n + 1)]                                # initial values
        u_0 = [u_0[1] - 2 * self.p(0) * dx] + u_0                # initial boundary values
        u.append(u_0)
        for j in range(1, m + 1):
            u_j = [self.node_val(u, k, i, j) for i in range(1, n + 1)]          # nodal values
            u_j = [u_j[1] - 2 * self.p(j * dt) * dx] + u_j + [self.q(j * dt)]        # boundary values
            u.append(u_j)
        u = np.delete(u, 0, 1)
        return u

    def get_k(self, dx: float, dt: float) -> float:
        return self.alpha * dt / dx ** 2

    @staticmethod
    def node_val(u: np.array, k: float, i: int, j: int) -> float:
        return u[j - 1][i] + k * (u[j - 1][i + 1] - 2 * u[j - 1][i] + u[j - 1][i - 1])

    def get_stable_m(self, L: float, n: int, t: float) -> int:
        m = np.ceil(2 * self.alpha * t * n ** 2 / (L ** 2))
        return int(m)
