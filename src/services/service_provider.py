from matplotlib.figure import Figure

from src.services.first_order_ode_service import FirstOrderODEService
from src.services.heat_equation_service import HeatEquationService
from src.services.second_order_ode_service import SecondOrderODEService
from src.services.wave_equation_service import WaveEquationService


class ServiceProvider:
    __figure: Figure
    __first_order_ode_service: FirstOrderODEService
    __second_order_ode_service: SecondOrderODEService
    __heat_equation: HeatEquationService
    __wave_equation: WaveEquationService

    def __init__(self):
        self.__figure = Figure(figsize=(6, 1), dpi=91.4)
        self.__first_order_ode_service = FirstOrderODEService(self.__figure)
        self.__second_order_ode_service = SecondOrderODEService(self.__figure)
        self.__heat_equation_service = HeatEquationService(self.__figure)
        self.__wave_equation_service = WaveEquationService(self.__figure)

    @property
    def main_figure(self):
        return self.__figure

    @property
    def first_order_ode_service(self):
        return self.__first_order_ode_service

    @property
    def second_order_ode_service(self):
        return self.__second_order_ode_service

    @property
    def heat_equation(self):
        return self.__heat_equation_service

    @property
    def wave_equation(self):
        return self.__wave_equation_service
