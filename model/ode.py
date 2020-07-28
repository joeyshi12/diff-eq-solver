import os
import abc
import xlsxwriter
import numpy as np
import matplotlib.pyplot as plt


class ODE:
    y: np.ndarray
    t_data: np.ndarray

    def __init__(self, f, filename):
        self.f = f
        self.filename = filename

    @abc.abstractmethod
    def solve(self, t, n):
        """computes solution into y as an array of size n+1"""
        pass

    def write_solution(self):
        """writes the values of y into a column inside of an xlsx file named filename"""
        table = np.column_stack((self.t_data, self.y))
        dirname = os.path.dirname(__file__)
        workbook = xlsxwriter.Workbook(os.path.join(dirname, '..', 'output', self.filename))
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 0, 't')
        worksheet.write(0, 1, 'y')
        row = 1
        for x_val, y_val in table:
            worksheet.write(row, 0, x_val)
            worksheet.write(row, 1, y_val)
            row += 1
        workbook.close()

    def plot_solution(self):
        """plots y onto a 2d figure as a function of t"""
        plt.plot(self.t_data, self.y)
        plt.show()

