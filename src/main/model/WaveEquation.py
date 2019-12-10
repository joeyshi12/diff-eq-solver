import numpy as np
import matplotlib.pyplot as plt


class WaveEquation:
    c: float
    boundary_condition: int
    # boundary_condition is one-of
    # 0, 1 ,2 ,3
    # Interp. - 0: Dirichlet BC
    #         - 1: Neumann BC
    #         - 2: Mixed 1 BC
    #         - 3: Mixed 2 BC

    def __init__(self, c: float, boundary_condition: int, initial_condition):
        self.c = c
        self.boundary_condition = boundary_condition
        self.initial_condition = initial_condition
