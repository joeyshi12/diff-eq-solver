import tkinter as tk


class Page(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

    def show(self):
        self.lift()
