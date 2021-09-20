import json
from os import listdir
from unittest import TestCase, main

from src.first_order_ode.first_order_ode import FirstOrderODE
from src.heat_equation.heat_equation import HeatEquation
from src.second_order_ode.second_order_ode import SecondOrderODE
from src.wave_equation.wave_equation import WaveEquation


class DifferentialEquationTest(TestCase):
    def setUp(self) -> None:
        self.queries = {}
        for file_name in listdir("queries"):
            name = file_name
            with open(f"./queries/{file_name}") as query:
                self.queries[name] = json.load(query)

    def test_solve(self):
        # TODO: implement test suite (#8)
        pass


if __name__ == '__main__':
    main()
