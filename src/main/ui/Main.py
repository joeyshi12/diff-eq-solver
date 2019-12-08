import matplotlib.pyplot as plt

from src.main.model.HeatEquation import HeatEquation

if __name__ == '__main__':
    # firstOrderODE = FirstOrderODE(lambda x, y: y, 1)
    # firstOrderODE.plot_solution(10, 1000)

    # secondOrderODE = SecondOrderODE(lambda x, y, y_prime: -y, 0, 1)
    # secondOrderODE.plot_solution(4*np.pi, 100)
    # x1, x2, y1, y2 = plt.axis()
    # plt.axis((x1,x2,-2,2))

    heatEquation = HeatEquation(1, 0, lambda x: 1 - (x - 1) ** 2)
    heatEquation.plot_solution(2, 50, 1)

    plt.show()
