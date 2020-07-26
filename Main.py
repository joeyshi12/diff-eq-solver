import os
import tkinter as tk
from ui.MainView import MainView

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Differential Equation Solver")
    dirname = os.path.dirname(__file__)
    photo = tk.PhotoImage(file=os.path.join(dirname, 'data', 'chiken.png'))
    root.iconphoto(False, photo)
    root.geometry("490x420")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
