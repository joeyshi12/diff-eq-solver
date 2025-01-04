import tkinter as tk

from diffeq_solver_tk.diffeq import BoundaryConditions, BoundaryCondition, HeatEquationMetadata, BoundaryType
from diffeq_solver_tk.ui.messages import common_messages, heat_equation_messages as messages
from diffeq_solver_tk.ui.forms import DifferentialEquationForm


class HeatEquationForm(DifferentialEquationForm):
    def __init__(self, master: tk.Frame, canvas, equation_service):
        DifferentialEquationForm.__init__(self, master, canvas, equation_service)
        tk.Label(master=self, text=common_messages.left_boundary_type).grid(row=0, column=0, pady=6, sticky="w")
        tk.Label(master=self, text=common_messages.right_boundary_type).grid(row=1, column=0, pady=6, sticky="w")

        self.left_boundary_type_variable = tk.StringVar(value=BoundaryType.DIRICHLET.value)
        left_dirichlet_button = tk.Radiobutton(master=self, text=common_messages.dirichlet, variable=self.left_boundary_type_variable, value=BoundaryType.DIRICHLET.value)
        left_neumann_button = tk.Radiobutton(master=self, text=common_messages.neumann, variable=self.left_boundary_type_variable, value=BoundaryType.NEUMANN.value)
        left_dirichlet_button.grid(row=0, column=1, sticky="w")
        left_neumann_button.grid(row=0, column=2, sticky="w")

        self.right_boundary_type_variable = tk.StringVar(value=BoundaryType.DIRICHLET.value)
        right_dirichlet_button = tk.Radiobutton(master=self, text=common_messages.dirichlet, variable=self.right_boundary_type_variable, value=BoundaryType.DIRICHLET.value)
        right_neumann_button = tk.Radiobutton(master=self, text=common_messages.neumann, variable=self.right_boundary_type_variable, value=BoundaryType.NEUMANN.value)
        right_dirichlet_button.grid(row=1, column=1, sticky="w")
        right_neumann_button.grid(row=1, column=2, sticky="w")

        self.left_boundary_values_entry = tk.Entry(master=self, width=24)
        self.right_boundary_values_entry = tk.Entry(master=self, width=24)
        self.initial_values_entry = tk.Entry(master=self, width=24)
        self.source_entry = tk.Entry(master=self, width=24)
        self.diffusivity_entry = tk.Entry(master=self, width=24)
        self.length_entry = tk.Entry(master=self, width=24)
        self.time_interval_entry = tk.Entry(master=self, width=24)
        self.samples_entry = tk.Entry(master=self, width=24)
        fields: list[tuple[str, str, tk.Entry]] = [
            (messages.left_boundary_values, messages.left_boundary_values_symbol, self.left_boundary_values_entry),
            (messages.right_boundary_values, messages.right_boundary_values_symbol, self.right_boundary_values_entry),
            (messages.initial_values, messages.initial_values_symbol, self.initial_values_entry),
            (messages.source_term, messages.source_term_symbol, self.source_entry),
            (messages.diffusivity, messages.diffusivity_symbol, self.diffusivity_entry),
            (messages.length, messages.length_symbol, self.length_entry),
            (messages.time_interval, messages.time_interval_symbol, self.time_interval_entry),
            (messages.samples, messages.samples_symbol, self.samples_entry)
        ]

        for i, (label_text, symbol, input_entry) in enumerate(fields):
            row = i + 2
            tk.Label(master=self, text=label_text + ":").grid(row=row, column=0, pady=6, sticky="w")
            tk.Label(master=self, text=symbol + " = ").grid(row=row, column=1, pady=0, sticky="e")
            input_entry.grid(row=row, column=2, columnspan=2)

        self.solve_button = tk.Button(master=self, text=common_messages.solve, width=10, command=self.solve_equation)
        self.export_button = tk.Button(master=self, text=common_messages.export, width=10, command=self.export_solution)
        self.render_plot_button = tk.Button(master=self, text=common_messages.show_plot, width=10, command=self.handle_render_plot)
        self.toggle_animation_button = tk.Button(master=self, text=common_messages.play, width=10, command=self.handle_toggle_animation)
        self.solve_button.grid(row=10, column=2, pady=6, sticky="w")

    def get_equation_metadata(self):
        left_boundary_type = BoundaryType(self.left_boundary_type_variable.get())
        right_boundary_type = BoundaryType(self.right_boundary_type_variable.get())
        boundary_conditions = BoundaryConditions(
            BoundaryCondition(left_boundary_type, self.left_boundary_values_entry.get()),
            BoundaryCondition(right_boundary_type, self.right_boundary_values_entry.get())
        )
        source = self.source_entry.get()
        return HeatEquationMetadata(
            boundary_conditions,
            float(self.length_entry.get()),
            int(self.samples_entry.get()),
            float(self.time_interval_entry.get()),
            float(self.diffusivity_entry.get()),
            self.initial_values_entry.get(),
            source if source else "0"
        )

    def on_solve(self):
        self.render_plot_button.grid(row=10, column=3, pady=6, sticky="e")
        self.toggle_animation_button.grid(row=11, column=3, pady=6, sticky="e")
        self.toggle_animation_button.configure(text=common_messages.play)
        self.export_button.grid(row=12, column=3, pady=6, sticky="e")

    def handle_render_plot(self):
        self.toggle_animation_button.configure(text=common_messages.play)
        self.equation_service.render_current_solution()
        self.canvas.draw()

    def handle_toggle_animation(self):
        self.equation_service.toggle_animation()
        self.canvas.draw()
        if self.equation_service.is_animation_playing():
            self.toggle_animation_button.configure(text=common_messages.pause)
        else:
            self.toggle_animation_button.configure(text=common_messages.play)

    def reset(self):
        self.equation_service.clear_solution()
        self.equation_service.clear_animation()
        self.canvas.draw()
        self.render_plot_button.grid_forget()
        self.toggle_animation_button.grid_forget()
        self.export_button.grid_forget()
