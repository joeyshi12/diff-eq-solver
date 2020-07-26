import os
import abc
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter


class ODE:
    def __init__(self, function, filename):
        self.function = function
        self.filename = filename

    def write_solution(self, L: float, n: int):
        """writes the solution over the domain [0,L] with n iterations"""
        x = np.linspace(0, L, n)
        y = self.solve(L, n)
        table = np.column_stack((x, y))
        dirname = os.path.dirname(__file__)
        workbook = xlsxwriter.Workbook(os.path.join(dirname, '..', 'excel_data', self.filename))
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 0, 'x')
        worksheet.write(0, 1, 'y')
        row = 1
        for x_val, y_val in table:
            worksheet.write(row, 0, x_val)
            worksheet.write(row, 1, y_val)
            row += 1
        workbook.close()

    def plot_solution(self, L: float, n: int):
        """plots the solution over the domain [0,L] with n iterations"""
        x = np.linspace(0, L, n)
        y = self.solve(L, n)
        plt.plot(x, y)

    @abc.abstractmethod
    def solve(self, L: float, n: int) -> np.array:
        """returns the solution over the domain [0,L] with n iterations"""
        pass
