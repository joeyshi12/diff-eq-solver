import numpy as np
from model.pde import PDE


class HeatEquation(PDE):
    def __init__(self, alpha, boundary_type, p, q, f):
        self.alpha = alpha
        super().__init__(boundary_type, p, q, "heat_equation_solution.xlsx")
        self.f = f

    def solve_dirichlet(self, dx, dt, n, m, k):
        """solves the heat equation with dirichlet boundary conditions"""
        self.u = np.zeros((m + 1, n + 1))
        self.u[0] = self.f(np.arange(n + 1) * dx)
        self.u[1:, 0] = self.p(np.arange(1, m + 1) * dt)
        self.u[1:, -1] = self.q(np.arange(1, m + 1) * dt)
        for j in range(1, m + 1):
            self.u[j, 1:n] = self.node_val(k, np.arange(1, n), j)

    def solve_neumann(self, dx, dt, n, m, k):
        """solves the heat equation with neumann boundary conditions"""
        self.u = np.zeros((m + 1, n + 3))
        self.u[0, 1:n + 2] = self.f(np.arange(n + 1) * dx)
        self.u[0, 0] = self.u[0, 1] - 2 * self.p(0) * dx
        self.u[0, -1] = self.u[0, -2] + 2 * self.q(0) * dx
        for j in range(1, m + 1):
            self.u[j, 1:n + 2] = self.node_val(k, np.arange(1, n + 2), j)
            self.u[j, 0] = self.u[j, 1] - 2 * self.p(j * dt) * dx
            self.u[j, -1] = self.u[j, -2] + 2 * self.q(j * dt) * dx
        self.u = np.delete(self.u, 0, axis=1)
        self.u = np.delete(self.u, -1, axis=1)

    def solve_mixed_1(self, dx, dt, n, m, k):
        """solves the heat equation with mixed 1 boundary conditions"""
        self.u = np.zeros((m + 1, n + 2))
        self.u[0, :n + 1] = self.f(np.arange(n + 1) * dx)
        self.u[1:, 0] = self.p(np.arange(1, m + 1) * dt)
        self.u[0, n + 1] = self.u[0, -2] + 2 * self.q(0) * dx
        for j in range(1, m + 1):
            self.u[j, 1:n + 1] = self.node_val(k, np.arange(1, n + 1), j)
            self.u[j, n + 1] = self.u[j, n - 1] + 2 * self.q(j * dt) * dx
        self.u = np.delete(self.u, -1, axis=1)

    def solve_mixed_2(self, dx, dt, n, m, k):
        """solves the heat equation with mixed 2 boundary conditions"""
        self.u = np.zeros((m + 1, n + 2))
        self.u[0, 1:n + 2] = self.f(np.arange(n + 1) * dx)
        self.u[0, 0] = self.u[0, 1] - 2 * self.p(0) * dx
        self.u[1:, -1] = self.q(np.arange(1, m + 1) * dt)
        for j in range(1, m + 1):
            self.u[j, 1:n + 1] = self.node_val(k, np.arange(n), j)
            self.u[j, 0] = self.u[j, 1] - 2 * self.p(j * dt) * dx
        self.u = np.delete(self.u, 0, axis=1)

    def k_val(self, dx, dt) -> float:
        """returns useful constant for computing node values"""
        return self.alpha * dt / dx ** 2

    def node_val(self, k, i, j) -> float:
        """computes solution value at index (j, i)"""
        return self.u[j - 1, i] + k * (self.u[j - 1, i + 1] - 2 * self.u[j - 1, i] + self.u[j - 1, i - 1])

    def get_stable_m(self, L, n, t) -> int:
        """computes value of m such that we get a stable solution"""
        m = np.ceil(2 * self.alpha * t * n ** 2 / (L ** 2))
        return int(m)
