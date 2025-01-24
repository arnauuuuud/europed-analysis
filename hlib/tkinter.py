import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

class FigureFrame(tk.Frame):
    def __init__(self, parent, *args, figure = None, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        if figure is None:
            self.fig = plt.figure()
        else:
            self.fig = figure

        self.canvas = FigureCanvasTkAgg(self.fig, master = self)
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        # After changing the plots, a call to FigureFrame.canvas.draw_idle() has to
        # be made to update

class ToggleButton(ttk.Button):
    """
    Toggle button where command should take a boolean which is true if the
    button is pressed and otherwise false
    """
    def __init__(self, parent, command = None, pressed = False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pressed = False
        self.command = command
        self.config(command = self.toggle_button)
        self.update_button()

    def update_button(self):
        if self.pressed:
            self.state(["pressed"])
        else:
            self.state(["!pressed"])

    def set_pressed(self, pressed):
        self.pressed = pressed
        self.update_button()
        if self.command is not None:
            self.command(self.pressed)

    def toggle_button(self):
        self.set_pressed(not self.pressed)

    def config(self, *args, **kwargs):
        if "command" in kwargs:
            self.command = kwargs["command"]
            kwargs.pop("command")
        super().config(*args, **kwargs)
