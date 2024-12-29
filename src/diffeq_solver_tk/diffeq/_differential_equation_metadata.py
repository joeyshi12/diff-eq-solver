from dataclasses import dataclass
from enum import Enum
from typing import Union


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
class OrdinaryDifferentialEquationMetadata:
    source: str
    initial_derivatives: list[float]
    samples: int
    time: float


@dataclass
class HeatEquationMetadata:
    boundary_conditions: BoundaryConditions
    length: float
    samples: int
    time: float
    alpha: float
    initial_values: str
    source: str = "0"


@dataclass
class WaveEquationMetadata:
    boundary_conditions: BoundaryConditions
    length: float
    samples: int
    time: float
    wave_speed: float
    initial_values: str
    initial_derivatives: str
    source: str = "0"


BoundedEquationMetadata = Union[HeatEquationMetadata, WaveEquationMetadata]
