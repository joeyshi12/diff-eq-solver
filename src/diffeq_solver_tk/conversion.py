from typing import Dict, Any

from diffeq_solver_tk.differential_equation_metadata import OrdinaryDifferentialEquationMetadata, HeatEquationMetadata, \
    BoundaryConditions, BoundaryCondition, BoundaryType, WaveEquationMetadata


def to_first_order_ode_metadata(query: Dict[str, Any]) -> OrdinaryDifferentialEquationMetadata:
    return OrdinaryDifferentialEquationMetadata(
        query["source"],
        query["initial_derivatives"],
        query["samples"],
        query["time"]
    )


def to_second_order_ode_metadata(query: Dict[str, Any]) -> OrdinaryDifferentialEquationMetadata:
    # TODO
    return OrdinaryDifferentialEquationMetadata("", [], 0, 0)


def to_heat_equation_metadata(query: Dict[str, Any]) -> HeatEquationMetadata:
    # TODO
    left_boundary_condition = BoundaryCondition(BoundaryType.DIRICHLET, "")
    right_boundary_condition = BoundaryCondition(BoundaryType.DIRICHLET, "")
    boundary_conditions = BoundaryConditions(left_boundary_condition, right_boundary_condition)
    return HeatEquationMetadata(boundary_conditions, 0, 0, 0, 0, "0")


def to_wave_equation_metadata(query: Dict[str, Any]) -> WaveEquationMetadata:
    # TODO
    left_boundary_condition = BoundaryCondition(BoundaryType.DIRICHLET, "")
    right_boundary_condition = BoundaryCondition(BoundaryType.DIRICHLET, "")
    boundary_conditions = BoundaryConditions(left_boundary_condition, right_boundary_condition)
    return WaveEquationMetadata(boundary_conditions, 0, 0, 0, 0, "0", "0")
