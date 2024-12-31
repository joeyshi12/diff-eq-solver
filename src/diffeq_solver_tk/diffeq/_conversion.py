from typing import Dict, Any

from diffeq_solver_tk.diffeq import OrdinaryDifferentialEquationMetadata, HeatEquationMetadata, \
    BoundaryConditions, BoundaryCondition, BoundaryType, WaveEquationMetadata


def to_ode_metadata(query: Dict[str, Any]) -> OrdinaryDifferentialEquationMetadata:
    # TODO: #14
    return OrdinaryDifferentialEquationMetadata(
        query["source"],
        query["initial_derivatives"],
        query["samples"],
        query["time"]
    )


def to_heat_equation_metadata(query: Dict[str, Any]) -> HeatEquationMetadata:
    # TODO: #14
    query_bc = query["boundary_conditions"]
    left_boundary_condition = BoundaryCondition(BoundaryType[query_bc["left"]["type"]], query_bc["left"]["values"])
    right_boundary_condition = BoundaryCondition(BoundaryType[query_bc["right"]["type"]], query_bc["right"]["values"])
    boundary_conditions = BoundaryConditions(left_boundary_condition, right_boundary_condition)
    return HeatEquationMetadata(
        boundary_conditions,
        query["length"],
        query["samples"],
        query["time"],
        query["alpha"],
        query["initial_values"],
        query.get("source", "0")
    )


def to_wave_equation_metadata(query: Dict[str, Any]) -> WaveEquationMetadata:
    # TODO: #14
    query_bc = query["boundary_conditions"]
    left_boundary_condition = BoundaryCondition(BoundaryType[query_bc["left"]["type"]], query_bc["left"]["values"])
    right_boundary_condition = BoundaryCondition(BoundaryType[query_bc["right"]["type"]], query_bc["right"]["values"])
    boundary_conditions = BoundaryConditions(left_boundary_condition, right_boundary_condition)
    return WaveEquationMetadata(
        boundary_conditions,
        query["length"],
        query["samples"],
        query["time"],
        query["wave_speed"],
        query["initial_values"],
        query["initial_derivatives"],
        query.get("source", "0")
    )
