from dataclasses import dataclass
from enum import Enum
from typing import List


class BoundaryType(Enum):
    DIRICHLET = "DIRICHLET"
    NEUMANN = "NEUMANN"


@dataclass
class BoundaryCondition:
    type: BoundaryType
    values: str


@dataclass
class BoundaryConditions:
    left: BoundaryCondition
    right: BoundaryCondition


@dataclass
class BoundedEquationMetadata:
    boundary_conditions: BoundaryConditions
    length: float
    samples: int
    time: float


@dataclass
class OrdinaryDifferentialEquationMetadata:
    source: str
    initial_derivatives: List[float]
    samples: int
    time: float


@dataclass
class HeatEquationMetadata(BoundedEquationMetadata):
    alpha: float
    initial_values: str
    source: str = "0"


@dataclass
class WaveEquationMetadata(BoundedEquationMetadata):
    wave_speed: float
    initial_values: str
    initial_derivatives: str
    source: str = "0"
