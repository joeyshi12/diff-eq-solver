import numpy as np
import matplotlib.pyplot as plt


class HeatEquation:
    alpha: float
    boundary_condition: int
    # boundary_condition is one-of
    # 0, 1 ,2 ,3
    # Interp. - 0: Dirichlet BC
    #         - 1: Neumann BC
    #         - 2: Mixed 1 BC
    #         - 3: Mixed 2 BC

    def __init__(self, alpha: float, boundary_condition: int):
        self.alpha = alpha
        self.boundary_condition = boundary_condition
