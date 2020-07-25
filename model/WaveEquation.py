import numpy as np

from model.PDE import PDE


class WaveEquation(PDE):
    c: float

    def __init__(self, c, boundary_type, p, q, f, g):
        self.c = c
        super().__init__(boundary_type, p, q)
        self.f = f
        self.g = g

    def solve_dirichlet(self, dx, dt, n, m, k):
        self.u = np.zeros((m + 2, n + 1))
        self.u[1] = self.f(np.arange(n + 1) * dx)
        self.u[0] = self.u[1] - 2 * dt * self.g(np.arange(n + 1) * dx)
        self.u[2:, 0] = self.p(np.arange(1, m + 1) * dt)
        self.u[2:, -1] = self.q(np.arange(1, m + 1) * dt)
        for j in range(2, m + 2):
            self.u[j, 1:n] = self.node_val(k, np.arange(1, n), j)
        self.u = np.delete(self.u, 0, axis=0)

    def solve_neumann(self, dx, dt, n, m, k):
        self.u = np.zeros((m + 2, n + 3))
        self.u[1, 1:n + 2] = self.f(np.arange(n + 1) * dx)
        self.u[0, 1:n + 2] = self.u[1, 1:n + 2] - 2 * dt * self.g(np.arange(n + 1) * dx)
        self.u[:2, 0] = self.u[:2, 1] - 2 * self.p(np.arange(-1, 1) * dt) * dx
        self.u[:2, -1] = self.u[:2, -2] - 2 * self.q(np.arange(-1, 1) * dt) * dx
        for j in range(2, m + 2):
            self.u[j, 1:n + 2] = self.node_val(k, np.arange(n + 1), j)
            self.u[j, 0] = self.u[j, 1] - 2 * self.p(j * dt) * dx
            self.u[j, -1] = self.u[j, -2] + 2 * self.q(j * dt) * dx
        self.u = np.delete(self.u, 0, axis=0)
        self.u = np.delete(self.u, 0, axis=1)
        self.u = np.delete(self.u, -1, axis=1)

    def solve_mixed_1(self, dx: float, dt: float, n: int, m: int, k: float):
        self.u = np.zeros((m + 2, n + 2))
        self.u[1, :n + 1] = self.f(np.arange(n + 1) * dx)
        self.u[0, :n + 1] = self.u[1, :n + 1] - 2 * dt * self.g(np.arange(n + 1) * dx)
        self.u[2:, 0] = self.p(np.arange(1, m + 1) * dt)
        self.u[:2, -1] = self.u[:2, -2] - 2 * self.q(np.arange(-1, 1) * dt) * dx
        for j in range(2, m + 2):
            self.u[j, 1:n + 1] = self.node_val(k, np.arange(1, n + 1), j)
            self.u[j, -1] = self.u[j, -2] + 2 * self.q(j * dt) * dx
        self.u = np.delete(self.u, 0, axis=0)
        self.u = np.delete(self.u, -1, axis=1)

    def solve_mixed_2(self, dx: float, dt: float, n: int, m: int, k: float):
        self.u = np.zeros((m + 2, n + 2))
        self.u[1, 1:n + 2] = self.f(np.arange(n + 1) * dx)
        self.u[0, 1:n + 2] = self.u[1, 1:n + 2] - 2 * dt * self.g(np.arange(n + 1) * dx)
        self.u[:2, 0] = self.u[:2, 1] - 2 * self.p(np.arange(-1, 1) * dt) * dx
        self.u[2:, -1] = self.q(np.arange(1, m + 1) * dt)
        for j in range(2, m + 2):
            self.u[j, 1:n + 2] = self.node_val(k, np.arange(n + 1), j)
            self.u[j, 0] = self.u[j, 1] - 2 * self.p(j * dt) * dx
        self.u = np.delete(self.u, 0, axis=0)
        self.u = np.delete(self.u, 0, axis=1)

    def k_val(self, dx, dt) -> float:
        return self.c * dt / dx

    def node_val(self, k, i, j) -> float:
        return k ** 2 * self.u[j - 1][i + 1] + 2 * (1 - k ** 2) * self.u[j - 1][i] + \
               k ** 2 * self.u[j - 1][i - 1] - self.u[j - 2][i]

    def get_stable_m(self, L, n, t) -> int:
        m = 4 * np.ceil(self.c * t * n / L)
        return int(m)