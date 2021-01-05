import tkinter as tk
from frontend.mainview import MainView

root = tk.Tk()
root.resizable(width=False, height=False)
root.title("DE Solver")
root.iconbitmap('assets/icon.ico')
root.geometry("1100x600")
main_view = MainView(root)
main_view.pack(side="top", fill="both", expand=True)
root.mainloop()
