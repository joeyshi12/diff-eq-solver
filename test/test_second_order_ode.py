import unittest

import numpy as np

from model.second_order_ode import SecondOrderODE


class TestSecondOrderODE(unittest.TestCase):
    def setUp(self) -> None:
        self.second_order_ode1 = SecondOrderODE(lambda t, y, z: -y, 0, 1)

    def test_solve(self):
        self.second_order_ode1.solve(4, 1000)

        t = np.linspace(0, 4, 1001)
        y1 = np.sin(t)

        np.testing.assert_array_almost_equal(self.second_order_ode1.y, y1, decimal=2)
