import abc
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter


class ODE:
    def __init__(self, function):
        self.function = function

    def write_solution(self, L: float, n: int):
        """writes the solution over the domain [0,L] with n iterations"""
        x = np.linspace(0, L, n)
        y = self.integrate(L, n)
        table = np.column_stack((x, y))
        workbook = xlsxwriter.Workbook('excel_data/ODE.xlsx')
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
        y = self.integrate(L, n)
        plt.plot(x, y)

    @abc.abstractmethod
    def integrate(self, L: float, n: int) -> np.array:
        """returns the solution over the domain [0,L] with n iterations"""
        pass
