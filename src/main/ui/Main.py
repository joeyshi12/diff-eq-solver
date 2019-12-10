import matplotlib.pyplot as plt
import numpy as np

from src.main.exception.BoundaryTypeException import EquationTypeException
from src.main.model.FirstOrderODE import FirstOrderODE
from src.main.model.HeatEquation import HeatEquation
from src.main.model.SecondOrderODE import SecondOrderODE


if __name__ == '__main__':
    # firstOrderODE = FirstOrderODE(lambda x, y: y, 1)
    # firstOrderODE.plot_solution(10, 1000)
    # firstOrderODE.write_solution(10, 100)

    # secondOrderODE = SecondOrderODE(lambda x, y, y_prime: -y, 0, 1)
    # secondOrderODE.plot_solution(4*np.pi, 100)
    # secondOrderODE.write_solution(4*np.pi, 100)
    # x1, x2, y1, y2 = plt.axis()
    # plt.axis((x1,x2,-2,2))

    p = lambda t: t
    q = lambda t: -t
    f = lambda x: 2 * x - x ** 2
    try:
        heatEquation = HeatEquation(1, 1, p, q, f)
        heatEquation.plot_solution(2, 25, 1)
        heatEquation.write_solution(2, 25, 1)
    except EquationTypeException:
        print("Invalid boundary type in heat equation")

    plt.show()
