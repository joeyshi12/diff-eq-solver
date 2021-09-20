from os import listdir
import unittest
import json
from src.solver.first_order_ode_solver import FirstOrderODESolver
from src.solver.second_order_ode_solver import SecondOrderODESolver
from src.solver.heat_equation_solver import HeatEquationSolver
from src.solver.wave_equation_1d import WaveEquation1D


class DifferentialEquationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.queries = {}
        for f in listdir("queries"):
            name = f.split(".")[0]
            with open("queries/" + f) as file:
                self.queries[name] = json.load(file)

    def test_solve(self):
        for name in self.queries.keys():
            if "initial_derivative" in self.queries[name]:
                diff_eq = SecondOrderODESolver(self.queries[name])
            elif "alpha" in self.queries[name]:
                diff_eq = HeatEquationSolver(self.queries[name])
            elif "c" in self.queries[name]:
                diff_eq = WaveEquation1D(self.queries[name])
            else:
                diff_eq = FirstOrderODESolver(self.queries[name])
            diff_eq.compute_solution()
            diff_eq.save_solution("outputs/" + name + ".xlsx")
        return True


if __name__ == '__main__':
    unittest.main()
