from tkinter import Frame, Entry, Variable, Label, StringVar, Radiobutton, Button
from typing import Generic, TypeVar, Union, Callable, Optional, Dict

import diffeq_solver_tk.messages.common_messages as common_messages
import diffeq_solver_tk.tkinter_config as config
from diffeq_solver_tk.differential_equation_metadata import BoundaryType

T = TypeVar('T')


class EquationFormBuilder(Generic[T]):
    __field_entry_map: Dict[T, Union[Entry, Variable]]

    def __init__(self, frame: Frame):
        self.frame = frame
        self.__field_entry_map = dict()

    def build_entry_row(self, field: T, display_name: str, symbol_name: str, row: int):
        self.__field_entry_map[field] = Entry(master=self.frame, font=config.details_font, width=24)
        self.__place_label(f"{display_name}:", row, 0, 18, "w")
        self.__place_label(f"{symbol_name} = ", row, 1, 0, "e")
        self.__field_entry_map[field].grid(row=row, column=2, columnspan=2)

    def build_boundary_type_section(self, left_boundary_type_field: T, right_boundary_type_field: T):
        self.__place_label(common_messages.left_boundary_type, 0, 0, 18, "w")
        self.__build_boundary_type_row(left_boundary_type_field, 0)
        self.__place_label(common_messages.right_boundary_type, 1, 0, 18, "w")
        self.__build_boundary_type_row(right_boundary_type_field, 1)

    def create_button(self, text: str, callback: Optional[Callable[[], None]] = None) -> Button:
        button = Button(
            master=self.frame,
            text=text,
            font=config.details_font,
            width=10,
        )
        if callback is not None:
            button.configure(command=callback)
        return button

    def get_field_entry_map(self) -> Dict[T, Union[Entry, Variable]]:
        return self.__field_entry_map

    def __place_label(self, text: str, row: int, column: int, horizontal_padding: int, sticky: str):
        Label(master=self.frame,
              text=text,
              font=config.details_font,
              background=config.details_background).grid(
            row=row, column=column, padx=horizontal_padding, pady=6, sticky=sticky)

    def __build_boundary_type_row(self, boundary_type_field: T, row: int):
        self.__field_entry_map[boundary_type_field] = StringVar(value=BoundaryType.DIRICHLET.value)
        self.__place_radio_button(common_messages.dirichlet,
                                  self.__field_entry_map[boundary_type_field],
                                  BoundaryType.DIRICHLET.value,
                                  row, 1)
        self.__place_radio_button(common_messages.neumann,
                                  self.__field_entry_map[boundary_type_field],
                                  BoundaryType.NEUMANN.value,
                                  row, 2)

    def __place_radio_button(self, text: str, variable: Variable, value: str, row: int, column: int):
        Radiobutton(master=self.frame,
                    text=text,
                    font=config.details_font,
                    background=config.details_background,
                    activebackground=config.details_background,
                    variable=variable,
                    value=value).grid(row=row, column=column, sticky="w")
