import unittest
from model.first_order_ode import *
import matplotlib.pyplot as plt


class TestFirstOrderODE(unittest.TestCase):
    def setUp(self) -> None:
        self.first_order_ode1 = FirstOrderODE(lambda t, y: -y, 1)
        self.first_order_ode2 = FirstOrderODE(lambda t, y: t - y, 0)

    def test_solve(self):
        self.first_order_ode1.solve(4, 1000)
        self.first_order_ode2.solve(4, 1000)

        t = np.linspace(0, 4, 1001)
        y1 = np.exp(-t)
        y2 = t - 1 + y1

        np.testing.assert_array_almost_equal(self.first_order_ode1.y, y1, decimal=2)
        np.testing.assert_array_almost_equal(self.first_order_ode2.y, y2, decimal=2)
