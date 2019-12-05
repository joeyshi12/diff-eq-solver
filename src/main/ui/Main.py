import numpy as np
import matplotlib.pyplot as plt

from src.main.model.FirstOrderODE import FirstOrderODE
from src.main.model.SecondOrderODE import SecondOrderODE

if __name__ == '__main__':
    second_order_ode = SecondOrderODE(lambda x, y, y_prime: -y, 0, 1)
    second_order_ode.plot_solution(10, 100)
