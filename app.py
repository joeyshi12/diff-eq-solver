import tkinter as tk

from src.differential_equation_messages import DifferentialEquationMessages
from src.main_view import MainView

if __name__ == "__main__":
    window = tk.Tk(className=DifferentialEquationMessages.title)
    window.resizable(width=False, height=False)
    # root.iconbitmap('assets/icon.ico')
    window.geometry("1100x600")
    main_view = MainView(window)
    main_view.pack(side="top", fill="both", expand=True)
    window.mainloop()
