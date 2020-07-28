import unittest

import numpy as np

from exception.boundary_type_exception import BoundaryTypeException
from model.wave_equation import WaveEquation


class TestWaveEquation(unittest.TestCase):
    def setUp(self) -> None:
        self.p1 = lambda t: 0
        self.q1 = lambda t: 0
        self.f1 = lambda x: 2 * x - x ** 2
        self.g1 = lambda x: x

        self.p2 = lambda t: t
        self.q2 = lambda t: 1
        self.f2 = lambda x: np.exp(-(x - 1) ** 2 / 2)
        self.g2 = lambda x: 0

    def test_solve_dirichlet(self):
        wave_equation_dirichlet1 = WaveEquation(1, 1, self.p1, self.q1, self.f1, self.g1)
        wave_equation_dirichlet2 = WaveEquation(1, 1, self.p2, self.q2, self.f2, self.g2)
        L = 2
        n = 16
        t = 1
        m = wave_equation_dirichlet1.get_stable_m(L, n, t)
        wave_equation_dirichlet1.solve(L, n, t, m)
        wave_equation_dirichlet2.solve(L, n, t, m)

        # Test Dimensions
        self.assertEqual(wave_equation_dirichlet1.u.shape, (m + 1, n + 1))
        self.assertEqual(wave_equation_dirichlet2.u.shape, (m + 1, n + 1))

        # Test Conditions
        np.testing.assert_array_equal(wave_equation_dirichlet1.u[0], self.f1(np.arange(n + 1) * (L / n)))
        np.testing.assert_array_equal(wave_equation_dirichlet1.u[1:, 0], self.p1(np.arange(1, m + 1) * (t / m)))
        np.testing.assert_array_equal(wave_equation_dirichlet1.u[1:, -1], self.q1(np.arange(1, m + 1) * (t / m)))
        np.testing.assert_array_equal(wave_equation_dirichlet2.u[0], self.f2(np.arange(n + 1) * (L / n)))
        np.testing.assert_array_equal(wave_equation_dirichlet2.u[1:, 0], self.p2(np.arange(1, m + 1) * (t / m)))
        np.testing.assert_array_equal(wave_equation_dirichlet2.u[1:, -1], self.q2(np.arange(1, m + 1) * (t / m)))

    def test_solve_neumann(self):
        wave_equation_neumann1 = WaveEquation(1, 2, self.p1, self.q1, self.f1, self.g1)
        wave_equation_neumann2 = WaveEquation(1, 2, self.p2, self.q2, self.f2, self.g2)
        L = 2
        n = 32
        t = 2
        m = wave_equation_neumann1.get_stable_m(L, n, t)
        wave_equation_neumann1.solve(L, n, t, m)
        wave_equation_neumann2.solve(L, n, t, m)

        # Test Dimensions
        self.assertEqual(wave_equation_neumann1.u.shape, (m + 1, n + 1))
        self.assertEqual(wave_equation_neumann2.u.shape, (m + 1, n + 1))

        # Test Conditions
        np.testing.assert_array_equal(wave_equation_neumann1.u[0], self.f1(np.arange(n + 1) * (L / n)))
        np.testing.assert_array_equal(wave_equation_neumann2.u[0], self.f2(np.arange(n + 1) * (L / n)))

    def test_solve_mixed_1(self):
        wave_equation_mixed_11 = WaveEquation(1, 3, self.p1, self.q1, self.f1, self.g1)
        wave_equation_mixed_12 = WaveEquation(1, 3, self.p2, self.q2, self.f2, self.g2)
        L = 2
        n = 24
        t = 1
        m = wave_equation_mixed_11.get_stable_m(L, n, t)
        wave_equation_mixed_11.solve(L, n, t, m)
        wave_equation_mixed_12.solve(L, n, t, m)

        # Test Dimensions
        self.assertEqual(wave_equation_mixed_11.u.shape, (m + 1, n + 1))
        self.assertEqual(wave_equation_mixed_12.u.shape, (m + 1, n + 1))

        # Test Conditions
        np.testing.assert_array_equal(wave_equation_mixed_11.u[0], self.f1(np.arange(n + 1) * (L / n)))
        np.testing.assert_array_equal(wave_equation_mixed_11.u[1:, 0], self.p1(np.arange(1, m + 1) * (t / m)))
        np.testing.assert_array_equal(wave_equation_mixed_12.u[0], self.f2(np.arange(n + 1) * (L / n)))
        np.testing.assert_array_equal(wave_equation_mixed_12.u[1:, 0], self.p2(np.arange(1, m + 1) * (t / m)))

    def test_solve_mixed_2(self):
        wave_equation_mixed_21 = WaveEquation(1, 4, self.p1, self.q1, self.f1, self.g1)
        wave_equation_mixed_22 = WaveEquation(1, 4, self.p2, self.q2, self.f2, self.g2)
        L = 2
        n = 40
        t = 3
        m = wave_equation_mixed_21.get_stable_m(L, n, t)
        wave_equation_mixed_21.solve(L, n, t, m)
        wave_equation_mixed_22.solve(L, n, t, m)

        # Test Dimensions
        self.assertEqual(wave_equation_mixed_21.u.shape, (m + 1, n + 1))
        self.assertEqual(wave_equation_mixed_22.u.shape, (m + 1, n + 1))

        # Test Conditions
        np.testing.assert_array_equal(wave_equation_mixed_21.u[0], self.f1(np.arange(n + 1) * (L / n)))
        np.testing.assert_array_equal(wave_equation_mixed_21.u[1:, -1], self.q1(np.arange(1, m + 1) * (t / m)))
        np.testing.assert_array_equal(wave_equation_mixed_22.u[0], self.f2(np.arange(n + 1) * (L / n)))
        np.testing.assert_array_equal(wave_equation_mixed_22.u[1:, -1], self.q2(np.arange(1, m + 1) * (t / m)))

    def test_integrate_invalid(self):
        wave_equation_invalid1 = WaveEquation(1, 5, self.p1, self.q1, self.f1, self.g1)
        wave_equation_invalid2 = WaveEquation(1, 5, self.p2, self.q2, self.f2, self.g2)
        L = 2
        n = 20
        t = 1
        m = wave_equation_invalid1.get_stable_m(L, n, t)
        try:
            wave_equation_invalid1.solve(L, n, t, m)
            wave_equation_invalid2.solve(L, n, t, m)
            self.fail("fail invalid boundary test")
        except BoundaryTypeException:
            print("pass invalid boundary test")