from tkinter import Tk
from diffeq_solver_tk.ui.messages import common_messages
from diffeq_solver_tk.ui.main_view import MainView


def main():
    app = Tk(className=common_messages.app_name)
    app.resizable(width=False, height=False)
    # app.iconbitmap('assets/icon.ico')
    app.geometry("1100x600")
    MainView(app).pack(side="top", fill="both", expand=True)
    app.mainloop()


if __name__ == "__main__":
    main()
