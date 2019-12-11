import abc

import numpy as np
import xlsxwriter
import matplotlib.pyplot as plt


class ODE:
    @abc.abstractmethod
    def integrate(self, L: float, n: int) -> np.array:
        pass

    def write_solution(self, L: float, n: int):
        x = np.linspace(0, L, n)
        y = self.integrate(L, n)
        table = np.column_stack((x, y))
        row = 1
        col = 0
        workbook = xlsxwriter.Workbook('excel_data/ODE.xlsx')
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 0, 'x')
        worksheet.write(0, 1, 'y')
        for x_val, y_val in table:
            worksheet.write(row, col, x_val)
            worksheet.write(row, col + 1, y_val)
            row += 1
        workbook.close()

    def plot_solution(self, L: float, n: int):
        x = np.linspace(0, L, n)
        y = self.integrate(L, n)
        plt.plot(x, y)
