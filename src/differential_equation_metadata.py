from dataclasses import dataclass
from enum import Enum


class DifferentialEquationMetadata:
    pass


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
class BoundedEquationMetadata(DifferentialEquationMetadata):
    boundary_conditions: BoundaryConditions


@dataclass
class FirstOrderODEMetadata(DifferentialEquationMetadata):
    source: str
    initial_value: float
    samples: int
    time: float


@dataclass
class SecondOrderODEMetadata(DifferentialEquationMetadata):
    source: str
    initial_value: float
    initial_derivative: float
    samples: int
    time: float


@dataclass
class HeatEquationMetadata(BoundedEquationMetadata):
    alpha: float
    length: float
    time: float
    samples: int
    initial_values: str
    source: str = "0"


@dataclass
class WaveEquationMetadata(BoundedEquationMetadata):
    c: float
    length: float
    time: float
    samples: int
    initial_values: str
    initial_derivatives: str
    source: str = "0"
