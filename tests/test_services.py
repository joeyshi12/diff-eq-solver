import numpy as np
from matplotlib.figure import Figure

from diffeq_solver_tk.diffeq import OrdinaryDifferentialEquationMetadata, HeatEquationMetadata, \
    BoundaryConditions, BoundaryCondition, BoundaryType, WaveEquationMetadata, \
    OrdinaryDifferentialEquationService, BoundedEquationService, \
    solve_first_order_ode, solve_second_order_ode, solve_heat_equation, solve_wave_equation


def test_first_order_ode_service():
    # TODO: add more assertions #8
    service = OrdinaryDifferentialEquationService(solve_first_order_ode, Figure())
    metadata = OrdinaryDifferentialEquationMetadata("-4 * x", [1], 50, 4)
    service.compute_and_update_solution(metadata)
    print(service.solution)
    assert service.solution[0] == 1


def test_second_order_ode_service():
    # TODO: add more assertions #8
    service = OrdinaryDifferentialEquationService(solve_second_order_ode, Figure())
    metadata = OrdinaryDifferentialEquationMetadata("-4 * x", [0, 1], 40, 5)
    service.compute_and_update_solution(metadata)
    assert service.solution[0] == 0


def test_heat_equation_service():
    # TODO: add more assertions #8
    service = BoundedEquationService(solve_heat_equation, Figure())
    metadata = HeatEquationMetadata(
        boundary_conditions=BoundaryConditions(
            BoundaryCondition(BoundaryType.NEUMANN, "t"),
            BoundaryCondition(BoundaryType.DIRICHLET, "1")
        ),
        length=1,
        samples=20,
        time=1,
        alpha=1,
        initial_values="0"
    )
    service.compute_and_update_solution(metadata)
    for i in range(20):
        assert service.solution[0, i] == 0


def test_wave_equation_service():
    # TODO: add more assertions #8
    service = BoundedEquationService(solve_wave_equation, Figure())
    metadata = WaveEquationMetadata(
        boundary_conditions=BoundaryConditions(
            BoundaryCondition(BoundaryType.NEUMANN, "t/2"),
            BoundaryCondition(BoundaryType.DIRICHLET, "0")
        ),
        length=1,
        samples=20,
        time=1,
        wave_speed=1,
        initial_values="np.sin(3*x)",
        initial_derivatives="x",
        source="np.exp(-t)*np.sin(x)+1"
    )
    service.compute_and_update_solution(metadata)
    expected = np.sin(3 * np.linspace(0, 1, 20))
    for i in range(20):
        assert service.solution[0, i] == expected[i]
