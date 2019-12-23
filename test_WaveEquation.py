import unittest

from exception.BoundaryTypeException import BoundaryTypeException
from model.WaveEquation import WaveEquation


class TestWaveEquation(unittest.TestCase):
    wave_equation_dirichlet: WaveEquation
    wave_equation_neumann: WaveEquation
    wave_equation_mixed_1: WaveEquation
    wave_equation_mixed_2: WaveEquation
    wave_equation_invalid: WaveEquation

    def setUp(self) -> None:
        p = lambda t: 0
        q = lambda t: 0
        f = lambda x: 2 * x - x ** 2
        g = lambda x: 0
        self.wave_equation_dirichlet = WaveEquation(1, 0, p, q, f, g)
        self.wave_equation_neumann = WaveEquation(1, 1, p, q, f, g)
        self.wave_equation_mixed_1 = WaveEquation(1, 2, p, q, f, g)
        self.wave_equation_mixed_2 = WaveEquation(1, 3, p, q, f, g)
        self.wave_equation_invalid = WaveEquation(1, 4, p, q, f, g)

    def test_integrate_dirichlet(self):
        L = 2
        n = 20
        t = 1
        m = self.wave_equation_dirichlet.get_stable_m(L, n, t)
        u_numerical = self.wave_equation_dirichlet.integrate(L, n, t, m)

        # Test Boundaries
        for j in range(m + 1):
            self.assertEqual(u_numerical[j][0], self.wave_equation_dirichlet.p(j))
            self.assertEqual(u_numerical[j][-1], self.wave_equation_dirichlet.q(j))

    def test_integrate_invalid(self):
        try:
            self.wave_equation_invalid.integrate(1, 1, 1, 1)
            self.fail("fail invalid boundary test")
        except BoundaryTypeException:
            print("pass invalid boundary test")