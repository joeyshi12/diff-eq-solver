import tkinter as tk
from diffeq_solver_tk.ui.messages import common_messages
from diffeq_solver_tk.ui.app import App


def main():
    min_width, min_height = 1100, 600
    root = tk.Tk(className=common_messages.app_name)
    root.geometry(f"{min_width}x{min_height}")
    root.minsize(min_width, min_height)
    # icon_image = tk.BitmapImage("assets/favicon.ico")
    # root.iconbitmap(icon_image)
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
