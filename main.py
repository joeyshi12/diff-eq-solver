import os
import tkinter as tk
from frontend.mainview import MainView


def main():
    root = tk.Tk()
    root.resizable(width=False, height=False)
    root.title("Differential Equation Solver")
    root.iconbitmap(os.path.join('assets/icon.ico'))
    root.geometry("552x540")
    main_view = MainView(root)
    main_view.pack(side="top", fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
