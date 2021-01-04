from os import listdir
from os.path import join
import unittest
import json
from backend.first_order_ode import FirstOrderODE
from backend.second_order_ode import SecondOrderODE
from backend.heat_equation_1d import HeatEquation1D
from backend.wave_equation_1d import WaveEquation1D


class DifferentialEquationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.queries = {}
        for f in listdir("queries"):
            name = f.split(".")[0]
            with open(join("queries", f)) as file:
                self.queries[name] = json.load(file)

    def test_solve(self):
        for name in self.queries.keys():
            if "initial_derivative" in self.queries[name]:
                diff_eq = SecondOrderODE(self.queries[name])
            elif "alpha" in self.queries[name]:
                diff_eq = HeatEquation1D(self.queries[name])
            elif "c" in self.queries[name]:
                diff_eq = WaveEquation1D(self.queries[name])
            else:
                diff_eq = FirstOrderODE(self.queries[name])
            diff_eq.solve()
            diff_eq.record_solution("../test/outputs/" + name + ".xlsx")
        return True


if __name__ == '__main__':
    unittest.main()
