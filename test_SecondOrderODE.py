import unittest

import numpy as np

from model.SecondOrderODE import SecondOrderODE


class TestSecondOrderODE(unittest.TestCase):
    test_ode: SecondOrderODE

    def setUp(self) -> None:
        self.test_ode = SecondOrderODE(lambda x, y, y_prime: -y, 0, 1)

    def test_integrate(self):
        y_numerical = self.test_ode.solve(2 * np.pi, 100)
        x = np.linspace(0, 2 * np.pi, 100)
        y_analytic = np.sin(x)

        # TODO: finish writing test
