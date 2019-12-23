import tkinter as tk

from ui.Page import Page


class WaveEquationPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Stub")
        label.grid(row=0, column=0)
