import numpy as np
from numpy import sin, cos, sinh, cosh, exp, e, pi
from backend.differential_equation import TimeDependent1D, InvalidQuery


class WaveEquation1D(TimeDependent1D):
    def __init__(self, query):
        if not self.is_valid(query):
            raise InvalidQuery
        super().__init__(query["boundary_condition"])
        initial_values = lambda x: eval(query["initial_condition"]["values"])
        initial_derivatives = lambda x: eval(query["initial_condition"]["derivatives"])
        if "source" in query:
            self.source = lambda t, x: eval(query["source"])
        else:
            self.source = lambda t, x: 0
        N = query["samples"]
        self.dx = query["length"] / (N - 1)
        K = 2 * np.int(query["c"] * query["time"] / self.dx) + 1
        self.dt = query["time"] / (K - 1)
        r = (query["c"] * self.dt / self.dx) ** 2
        self.D = np.zeros((N - 2, N))
        for i in range(N - 2):
            self.D[i, i] = r
            self.D[i, i + 1] = 2 * (1 - r)
            self.D[i, i + 2] = r
        self.solution = np.zeros((K, N))
        self.solution[0] = initial_values(np.arange(N) * self.dx)
        self.solution[1, 1:N - 1] = 0.5 * self.D @ self.solution[0]
        self.solution[1, 1:N - 1] += self.dt ** 2 * initial_derivatives(np.arange(1, N - 1) * self.dx)
        self.solution[1, 1:N - 1] += 0.5 * self.dt ** 2 * self.source(self.dt, np.arange(1, N - 1) * self.dx)
        self._solve_boundary(1)

    def is_valid(self, query):
        return query["samples"] > 1 and query["length"] > 0 and query["time"] > 0

    def solve(self):
        K, N = self.solution.shape
        for k in range(2, K):
            self.solution[k, 1:N - 1] = self.D @ self.solution[k - 1] - self.solution[k - 2, 1:N - 1]
            self.solution[k, 1:N - 1] += self.dt ** 2 * self.source(k * self.dt, np.arange(1, N - 1) * self.dx)
            self._solve_boundary(k)