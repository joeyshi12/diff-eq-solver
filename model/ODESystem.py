import os
import xlsxwriter
import numpy as np
import matplotlib.pyplot as plt


class ODESystem:
    x: np.ndarray
    y: np.ndarray
    t_data: np.ndarray

    def __init__(self, f, g, initial_x, initial_y):
        self.f = f
        self.g = g
        self.initial_x = initial_x
        self.initial_y = initial_y

    def solve(self, t, n):
        """computes solution into x and y as arrays of size n+1"""
        dt = t / n
        self.t_data = np.arange(n + 1) * dt
        self.x = np.zeros(n + 1)
        self.y = np.zeros(n + 1)
        self.x[0] = self.initial_x
        self.y[0] = self.initial_y
        for i in range(1, n + 1):
            self.x[i] = self.x[i - 1] + self.f(i * dt, self.x[i - 1], self.y[i - 1])
            self.y[i] = self.y[i - 1] + self.g(i * dt, self.x[i - 1], self.y[i - 1])

    def write_solution(self):
        """writes the values of x and y into separate columns inside of an xlsx file named ODESystem.xlsx"""
        table = np.column_stack((self.t_data, self.x, self.y))
        dirname = os.path.dirname(__file__)
        workbook = xlsxwriter.Workbook(os.path.join(dirname, '..', 'output', 'ODESystem.xlsx'))
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, 't')
        worksheet.write(0, 1, 'x')
        worksheet.write(0, 2, 'y')
        row = 1
        for t_val, x_val, y_val in table:
            worksheet.write(row, 0, t_val)
            worksheet.write(row, 1, x_val)
            worksheet.write(row, 2, y_val)
            row += 1
        workbook.close()

    def plot_solution(self):
        """plots (x, y) onto a 2d figure"""
        plt.plot(self.x, self.y)
        plt.show()
