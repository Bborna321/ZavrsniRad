from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
from classes.components.menubar import *
import matplotlib
import tkinter as tk
from tkinter import ttk
from components.animate import *
import global_vars as gv

matplotlib.use('TkAgg')


def turnOnOffMacd():
    print("jesam u ovoj funkciji")
    if gv.macdOnOff=="off":
        gv.macdOnOff="on"
    elif gv.macdOnOff=="on":
        gv.macdOnOff="off"


class Window_tkinter(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self,default='@./mario.xbm')
        tk.Tk.wm_title(self, "Bot 'n' stuff")

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = Menubar(container)
        tk.Tk.config(self, menu=menubar)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for frame in (FirstPage, SettingsPage, GraphPage):
            newFrame = frame(container, self)
            self.frames[frame] = newFrame
            newFrame.grid(row=0, column=0, sticky='news')
        self.show_frame(GraphPage)

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

        label1 = tk.Label(self, text='Page One', font=large_font)
        label1.pack(pady=25, padx=25)
        # label11 = tk.Label(self, text='Description')
        # label11 .pack()

        button1 = ttk.Button(self, text="Confirm",
                             command=lambda: controller.show_frame(FirstPage))
        button2 = ttk.Button(self, text="Revert",
                             command=lambda: controller.show_frame(FirstPage))
        button1.pack()
        button2.pack()


class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page")
        label.pack()

        market_name = ttk.Entry(self, textvariable="username")
        market_name.pack()

        button2 = tk.Button(self, text="goto First Page",
                            command=lambda: controller.show_frame(FirstPage))
        button2.pack()
        button3 = tk.Button(self, text="Settings",
                            command=lambda: controller.show_frame(SettingsPage))
        button3.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        button4 = tk.Button(self, text="draw graph", command=lambda: 1 + 1)
        button4.pack()


