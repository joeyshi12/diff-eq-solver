import argparse
import json

from diffeq_solver_tk import __version__
from diffeq_solver_tk.diffeq import to_ode_metadata, to_heat_equation_metadata, to_wave_equation_metadata, \
    solve_first_order_ode, solve_second_order_ode, solve_heat_equation, solve_wave_equation
from diffeq_solver_tk.excel_export import export_ode_solution, export_bounded_equation_solution


def write_solution(infile: str, outfile: str, equation_type: str):
    with open(infile) as file:
        query = json.load(file)
        match equation_type:
            case "ode1" | "ode2":
                metadata = to_ode_metadata(query)
                solution = solve_first_order_ode(metadata) \
                    if equation_type == "ode1" \
                    else solve_second_order_ode(metadata)
                export_ode_solution(solution, metadata, outfile)
            case "heat":
                metadata = to_heat_equation_metadata(query)
                solution = solve_heat_equation(metadata)
                export_bounded_equation_solution(solution, metadata, outfile)
            case "wave":
                metadata = to_wave_equation_metadata(query)
                solution = solve_wave_equation(metadata)
                export_bounded_equation_solution(solution, metadata, outfile)
            case _:
                raise Exception(f"Invalid equation type {equation_type}")


def main():
    parser = argparse.ArgumentParser(description="Numerically solves differential equations.")
    parser.add_argument("-V", "--version", action="store_true", help="Show version and exit")
    parser.add_argument("type", type=str, choices=["ode1", "ode2", "heat", "wave"], help="DE type to solve")
    parser.add_argument("infile", type=str, help="DE metadata source file path")
    parser.add_argument("outfile", type=str, help="Solution output file path", default="solution.xlsx")
    args = parser.parse_args()

    if args.version:
        print(f"diffeq-solver-tk {__version__}")
        return

    write_solution(args.infile, args.outfile, args.type)


if __name__ == "__main__":
    main()
