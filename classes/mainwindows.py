from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
from classes.components.menubar import *
from classes.animate import *
from classes.components.datamanager import *
from tkinter import *
import tkinter as tk
import matplotlib;

matplotlib.use("TkAgg")


class Window_tkinter(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Bot 'n' stuff")

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = Menubar(container)
        tk.Tk.config(self, menu=menubar)

        self.__CreateFrames(container)
        self.show_frame(SettingsPage)

    def __CreateFrames(self, container):
        self.frames = {}

        for frame in (FirstPage, SettingsPage, GraphPage):
            newFrame = frame(container, self)
            self.frames[frame] = newFrame
            newFrame.grid(row=0, column=0, sticky='news')

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label0 = tk.Label(self, text='Litecoin trading application', font=large_font)
        label0.pack(pady=25, padx=25)

        button0 = ttk.Button(self, text="Agree",
                             command=lambda: controller.show_frame(GraphPage))
        button0.pack()
        button02 = ttk.Button(self, text="Disagree",
                              command=lambda: quit())
        button02.pack()


class SettingsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Options(self, controller, GraphPage)


class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.pause = False
        button1 = tk.Button(self, text="Pause",
                            command=self.onClick)
        button1.pack()

        button2 = tk.Button(self, text="Animate",
                            command=self.__DrawGraph)
        button2.pack()

        button3 = tk.Button(self, text="Settings",
                            command=controller.show_frame(SettingsPage))
        button3.pack()


    def onClick(self):
        self.pause = not self.pause

    def __DrawGraph(self):
        fig = mpf.figure(style='charles', figsize=(7, 8))
        ax1 = fig.add_subplot()

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        ani = animation.FuncAnimation(fig, lambda _: animate(_, ani, ax1, self.pause), interval=50)