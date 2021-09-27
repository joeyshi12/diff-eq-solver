from tkinter import Tk

import src.messages.common_messages as common_messages
from src.main_view import MainView


def main():
    app = Tk(className=common_messages.app_name)
    app.resizable(width=False, height=False)
    # app.iconbitmap('assets/icon.ico')
    app.geometry("1100x600")
    MainView(app).pack(side="top", fill="both", expand=True)
    app.mainloop()


if __name__ == "__main__":
    main()
