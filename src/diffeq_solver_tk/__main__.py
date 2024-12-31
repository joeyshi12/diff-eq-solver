import tkinter as tk
from diffeq_solver_tk.ui.messages import common_messages
from diffeq_solver_tk.ui.app import App


def main():
    root = tk.Tk(className=common_messages.app_name)
    root.geometry("1100x600")
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
