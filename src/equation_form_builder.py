from tkinter import Frame, Entry, Variable, Label, StringVar, Radiobutton
from typing import Generic, TypeVar, Union

from src.differential_equation_metadata import BoundaryType
import src.tkinter_config as config

T = TypeVar('T')


class EquationFormBuilder(Generic[T]):
    __field_entry_map: dict[T, Union[Entry, Variable]]

    def __init__(self, frame: Frame):
        self.frame = frame
        self.__field_entry_map = dict()

    def build_entry_row(self, field: T, display_name: str, symbol_name: str, row: int):
        self.__field_entry_map[field] = Entry(master=self.frame, font=config.details_font)
        Label(self.frame, text=f"{display_name}:", font=config.details_font, background=config.details_background).grid(
            row=row, column=0, padx=18, pady=10, sticky="w")
        Label(self.frame, text=f"{symbol_name} = ", font=config.details_font, background=config.details_background).grid(
            row=row, column=1, padx=0, pady=10, sticky="e")
        self.__field_entry_map[field].grid(row=row, column=2, pady=0)

    def build_boundary_type_section(self, left_boundary_type_field: T, right_boundary_type_field: T):
        self.__build_boundary_type_row(left_boundary_type_field, 0)
        self.__build_boundary_type_row(right_boundary_type_field, 1)

    def get_field_entry_map(self):
        return self.__field_entry_map

    def __build_boundary_type_row(self, boundary_type_field: T, row: int):
        self.__field_entry_map[boundary_type_field] = StringVar(value=BoundaryType.DIRICHLET.value)
        self.__place_radio_button(
            "dirichlet", self.__field_entry_map[boundary_type_field], row, 1, BoundaryType.DIRICHLET.value)
        self.__place_radio_button(
            "neumann", self.__field_entry_map[boundary_type_field], row, 2, BoundaryType.DIRICHLET.value)

    def __place_radio_button(self, text: str, variable: Variable, row: int, column: int, value: str):
        Radiobutton(master=self.frame,
                    text=text,
                    font=config.details_font,
                    background=config.details_background,
                    activebackground=config.details_background,
                    variable=variable,
                    value=value).grid(row=row, column=column, sticky="w")
