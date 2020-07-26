import unittest
from model.FirstOrderODE import *


class TestFirstOrderODE(unittest.TestCase):
    test_ode: FirstOrderODE

    def setUp(self) -> None:
        self.test_ode = FirstOrderODE(lambda x, y: -y, 1)

    def test_integrate(self):
        self.test_ode.solve(1, 100)
        x = np.linspace(0, 1, 100)
        y_analytic = np.e ** -x

        # TODO: finish writing test
