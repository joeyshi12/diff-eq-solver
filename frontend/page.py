import tkinter as tk


class Page(tk.Frame):
    bgcolor = '#BFC0C0'
    font = ("Verdana", 10)

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.configure(background=self.bgcolor)

    def show(self):
        self.lift()
