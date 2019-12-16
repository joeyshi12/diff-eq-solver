import unittest

import numpy as np

from src.main.model.SecondOrderODE import SecondOrderODE


class SecondOrderODETest(unittest.TestCase):
    test_ode: SecondOrderODE

    def setUp(self) -> None:
        self.test_ode = SecondOrderODE(lambda x, y, y_prime: -y, 0, 1)

    def test_integrate(self):
        y_numerical = self.test_ode.integrate(2 * np.pi, 100)
        x = np.linspace(0, 2 * np.pi, 100)
        y_analytic = np.sin(x)

        # TODO: finish writing test
