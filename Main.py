import tkinter as tk

from ui.MainView import MainView

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Differential Equation Solver")
    root.geometry("490x400")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
