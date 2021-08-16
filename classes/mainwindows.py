from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
from classes.components.menubar import *
from classes.animate import *
from classes.tactics import *
import classes.money_manager
from classes.components.datamanager import *
from tkinter import *
import tkinter as tk
from tkinter import ttk
import matplotlib

matplotlib.use("TkAgg")


class Window_tkinter(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Bot 'n' stuff")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


        container = tk.Frame(self)
        container.grid(column=0, row=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        menubar = Menubar(container)
        tk.Tk.config(self, menu=menubar)

        self.__CreateFrames(container)
        self.show_frame(GraphPage)

    def __CreateFrames(self, container):
        self.frames = {}

        for frame in (FirstPage, GraphPage):
            newFrame = frame(container, self)
            self.frames[frame] = newFrame
            newFrame.grid(row=0, column=0, sticky=NSEW)
            newFrame.columnconfigure(0, weight=1)
            newFrame.rowconfigure(0, weight=1)

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


# class SettingsPage(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         Options(self, controller, GraphPage)


class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.pause = False
        self.frame1 = Frame(self)
        self.frame1.grid(column=3, row=0, rowspan=1, columnspan=1, sticky=NW)
        self.frame2 = Frame(self, bg="blue")
        self.frame2.grid(column=0,row=0, sticky=NSEW)
        self.frame3 = Frame(self.frame1)
        self.money_manager = classes.money_manager.Money_manager(gv.current_money,gv.sell_at_high,gv.sell_at_low)
        self.options = Options(self.frame3, controller,self.money_manager)
        self.frame3.grid(column=0, row=1, sticky=NSEW)

        self.frame1.rowconfigure(0,weight=1)
        button1 = tk.Button(self.frame1, text="Pause", command=self.PauseAnimation)
        button1.grid(column=0, row=0, sticky=NW)

        button2 = tk.Button(self.frame1, text="Animate", command=lambda: self.__DrawGraph(self.money_manager))
        button2.grid(column=1, row=0, sticky=NW)



    def PauseAnimation(self):
        self.pause = not self.pause

    def __DrawGraph(self,money_manager):
        print("tu")
        fig = mpf.figure(style='charles', figsize=(7, 8))
        ax1 = fig.add_subplot()

        canvas = FigureCanvasTkAgg(fig, self.frame2)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, columnspan=3, rowspan=3, sticky=NSEW)
        canvas.get_tk_widget().columnconfigure(0, weight=1)
        canvas.get_tk_widget().rowconfigure(0, weight=1)
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.rowconfigure(0, weight=1)


        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        fig.canvas.mpl_connect('close_event', print("close"))
        tactic = Tactics(ax1)
        #money_manager = classes.money_manager.Money_manager(gv.current_money,gv.sell_at_high,gv.sell_at_low)
        ani = animation.FuncAnimation(fig, lambda _: animate(_, ani, ax1, self.pause, self.options.toAnimate, tactic, money_manager), interval=3000)
