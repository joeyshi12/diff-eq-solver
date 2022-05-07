import argparse
import json
from tkinter import Tk
from typing import List

import diffeq_solver_tk.messages.common_messages as common_messages
from diffeq_solver_tk import __version__
from diffeq_solver_tk.conversion import to_first_order_ode_metadata, to_second_order_ode_metadata, \
    to_heat_equation_metadata, to_wave_equation_metadata
from diffeq_solver_tk.finite_difference import solve_first_order_ode, solve_second_order_ode, solve_heat_equation, \
    solve_wave_equation
from diffeq_solver_tk.util import export_ode_solution, export_bounded_equation_solution
from .main_view import MainView

first_order_ode_option = "ode1"
second_order_ode_option = "ode2"
heat_equation_option = "heat"
wave_equation_option = "wave"

de_options: List[str] = [
    first_order_ode_option,
    second_order_ode_option,
    heat_equation_option,
    wave_equation_option
]

conversion_map = {
    first_order_ode_option: to_first_order_ode_metadata,
    second_order_ode_option: to_second_order_ode_metadata,
    heat_equation_option: to_heat_equation_metadata,
    wave_equation_option: to_wave_equation_metadata
}

solve_map = {
    first_order_ode_option: solve_first_order_ode,
    second_order_ode_option: solve_second_order_ode,
    heat_equation_option: solve_heat_equation,
    wave_equation_option: solve_wave_equation
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version", action="store_true", help="Show version and exit")
    subparsers = parser.add_subparsers(dest="command")
    solve_parser = subparsers.add_parser("solve")
    solve_parser.add_argument("type", type=str, choices=de_options, help="DE type to solve")
    solve_parser.add_argument("infile", type=str, help="DE metadata source file path")
    solve_parser.add_argument("outfile", type=str, help="Solution output file path", default="solution.xlsx")
    args = parser.parse_args()

    if args.version:
        print(f"diffeq-solver-tk {__version__}")
    elif args.command == "solve":
        with open(args.infile) as f:
            query = json.load(f)
            metadata = conversion_map[args.type](query)
            solution = solve_map[args.type](metadata)
            if args.type == first_order_ode_option or args.type == second_order_ode_option:
                export_ode_solution(solution, metadata, args.outfile)
            else:
                export_bounded_equation_solution(solution, metadata, args.outfile)
    else:
        app = Tk(className=common_messages.app_name)
        app.resizable(width=False, height=False)
        # app.iconbitmap('assets/icon.ico')
        app.geometry("1100x600")
        MainView(app).pack(side="top", fill="both", expand=True)
        app.mainloop()


if __name__ == "__main__":
    main()
