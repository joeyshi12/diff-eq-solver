import unittest

import numpy as np

from exception.BoundaryTypeException import BoundaryTypeException
from model.HeatEquation import HeatEquation


class HeatEquationTest(unittest.TestCase):
    heat_equation_dirichlet: HeatEquation
    heat_equation_neumann: HeatEquation
    heat_equation_mixed_1: HeatEquation
    heat_equation_mixed_2: HeatEquation
    heat_equation_invalid: HeatEquation

    def setUp(self) -> None:
        p = lambda t: 0
        q = lambda t: 0
        f = lambda x: 2 * x - x ** 2
        self.heat_equation_dirichlet = HeatEquation(1, 0, p, q, f)
        self.heat_equation_neumann = HeatEquation(1, 1, p, q, f)
        self.heat_equation_mixed_1 = HeatEquation(1, 2, p, q, f)
        self.heat_equation_mixed_2 = HeatEquation(1, 3, p, q, f)
        self.heat_equation_invalid =  HeatEquation(1, 4, p, q, f)

    def test_integrate_dirichlet(self):
        L = 2
        n = 20
        t = 1
        m = np.ceil(2 * self.heat_equation_dirichlet.alpha * t * n ** 2 / (L ** 2))
        m = int(m)
        u_numerical = self.heat_equation_dirichlet.integrate(L, n, t, m)

        # Test Boundaries
        for j in range(m + 1):
            self.assertEquals(u_numerical[j][0], self.heat_equation_dirichlet.p(j))
            self.assertEquals(u_numerical[j][-1], self.heat_equation_dirichlet.q(j))

    def test_integrate_invalid(self):
        try:
            self.heat_equation_invalid.integrate(1, 1, 1, 1)
            self.fail("fail invalid boundary test")
        except BoundaryTypeException:
            print("pass invalid boundary test")