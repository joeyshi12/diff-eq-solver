import tkinter as tk

from src.main_view import MainView


def main():
    app = tk.Tk(className="Differential Equation Solver")
    app.resizable(width=False, height=False)
    # app.iconbitmap('assets/icon.ico')
    app.geometry("1100x600")
    MainView(app).pack(side="top", fill="both", expand=True)
    app.mainloop()


if __name__ == "__main__":
    main()
