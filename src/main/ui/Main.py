import matplotlib.pyplot as plt
import numpy as np

from src.main.exception.BoundaryTypeException import BoundaryTypeException
from src.main.model.FirstOrderODE import FirstOrderODE
from src.main.model.HeatEquation import HeatEquation
from src.main.model.SecondOrderODE import SecondOrderODE
from src.main.model.WaveEquation import WaveEquation

if __name__ == '__main__':
    # firstOrderODE = FirstOrderODE(lambda x, y: y, 1)
    # firstOrderODE.plot_solution(10, 1000)
    # firstOrderODE.write_solution(10, 100)

    # secondOrderODE = SecondOrderODE(lambda x, y, y_prime: -y, 0, 1)
    # secondOrderODE.plot_solution(4*np.pi, 100)
    # secondOrderODE.write_solution(4*np.pi, 100)
    # x1, x2, y1, y2 = plt.axis()
    # plt.axis((x1,x2,-2,2))

    p = lambda t: 0               # Left Boundary
    q = lambda t: 0               # Right Boundary
    f = lambda x: 2 * x - x ** 2  # Initial Values
    heatEquation = HeatEquation(1, 0, p, q, f)
    L = 2
    n = 25
    t = 1
    m = heatEquation.get_stable_m(L, n, t)
    try:
        heatEquation.plot_solution(L, n, t, m)
        heatEquation.write_solution(L, n, t, m)
    except BoundaryTypeException:
        print("Invalid boundary type in heat equation")

    # p = lambda t: 2                 # Left Boundary
    # q = lambda t: 2                 # Right Boundary
    # f = lambda x: 2 * x - x ** 2    # Initial Values
    # g = lambda x: 0                 # Initial Derivatives
    # waveEquation = WaveEquation(1, 1, p, q, f, g)
    # L = 2
    # n = 100
    # t = 2
    # m = waveEquation.get_stable_m(L, n, t)
    # try:
    #     waveEquation.plot_solution(L, n, t, m)
    #     waveEquation.write_solution(L, n, t, m)
    # except BoundaryTypeException:
    #     print("Invalid boundary type in wave equation")

    plt.show()
