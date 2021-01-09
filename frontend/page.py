import tkinter as tk


class Page(tk.Frame):
    font = ("Verdana", 10)

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.fig = root.fig
        self.canvas = root.canvas
        self.bgcolour = root.bgcolour
        self.root = root
        self.configure(background=self.bgcolour)

    def show(self):
        self.root.pause_animation()
        self.lift()
