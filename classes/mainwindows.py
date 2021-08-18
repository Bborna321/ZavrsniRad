from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from classes.components.menubar import *
from classes.animate import *
from classes.tactics import *
import classes.money_manager
import matplotlib
from classes.components.sidebar import *

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

        for frame in [GraphPage]:
            newFrame = frame(container, self)
            self.frames[frame] = newFrame
            newFrame.grid(row=0, column=0, sticky=NSEW)
            newFrame.columnconfigure(0, weight=1)
            newFrame.rowconfigure(0, weight=1)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.animation = False
        self.pause = False
        self.buttonstate = 'normal'
        self.speed=1000

        self.__CreateFrames(controller)

        CreateJson()
        self.tactic = Tactics(self.ax1, self.mylist, self.options, self.money_manager)
        self.__CreateCanvas()

    def PauseAnimation(self):
        self.pause = not self.pause

    def ChangeSpeed(self, multiplier):
        if 50 <= self.speed*multiplier <= 1000:
            self.speed = self.speed*multiplier
            self.ani.event_source.interval = self.speed
            print(self.ani.event_source.interval)


    def __CreateFrames(self, controller):
        self.fig = mpf.figure(style='charles', figsize=(7, 8))
        self.ax1 = self.fig.add_subplot()

        self.animationFrame = Frame(self, bg="black")
        self.animationFrame.grid(column=0, row=0, sticky=NSEW)
        self.animationFrame.columnconfigure(0, weight=1)
        self.animationFrame.rowconfigure(1, weight=1)

        self.buttonsFrame = Frame(self.animationFrame, bg="blue")
        self.buttonsFrame.grid(column=0, row=0, columnspan=3, rowspan=1, sticky=NSEW)


        self.graphFrame = Frame(self.animationFrame, bg="blue")
        self.graphFrame.grid(column=0, row=0, columnspan=3, rowspan=3, sticky=NSEW)
        self.graphFrame.columnconfigure(0, weight=1)
        self.graphFrame.rowconfigure(0, weight=1)

        self.informationFrame = Frame(self, bg='red')
        self.informationFrame.grid(column=3, row=0, rowspan=3, columnspan=1, sticky=NSEW)

        self.pauseButton = tk.Button(self.informationFrame, text="\u23F8", command=self.PauseAnimation)
        self.pauseButton.grid(column=0, row=0, columnspan=1, sticky=NSEW)

        self.animateButton = tk.Button(self.informationFrame, text='\u23F5', command=lambda: self.__DrawGraph(self.money_manager))
        self.animateButton.grid(column=1, row=0, columnspan=1, rowspan=1, sticky=NSEW)

        self.slowerButton = tk.Button(self.informationFrame, text='\u23EA', command=lambda: self.ChangeSpeed(2.0))
        self.slowerButton.grid(column=2, row=0, columnspan=1, rowspan=1, sticky=NSEW)

        self.fasterButton = tk.Button(self.informationFrame, text='\u23E9', command=lambda: self.ChangeSpeed(0.5))
        self.fasterButton.grid(column=3, row=0, columnspan=1, rowspan=1, sticky=NSEW)

        self.resetButton = tk.Button(self.informationFrame, text="\u23F9",
                                     command=lambda: self.__DrawGraph(self.money_manager), state='disabled')
        self.resetButton.grid(column=4, row=0, columnspan=1, sticky=NSEW)

        self.settings = Frame(self.informationFrame)
        self.settings.grid(column=0, row=1, columnspan=5, rowspan=1, sticky=NSEW)

        self.console = Frame(self.informationFrame, bg='yellow')
        self.console.grid(column=0, row=2, columnspan=5, rowspan=3, sticky=NSEW)
        self.informationFrame.rowconfigure(2, weight=1)

        self.scrollbar = Scrollbar(self.console)
        self.scrollbar.grid(row=0, column=6, rowspan=1, sticky=NS)

        self.mylist = Listbox(self.console, yscrollcommand=self.scrollbar.set)
        self.mylist.grid(row=0, column=0, columnspan=4, sticky=NSEW)
        self.scrollbar.config(command=self.mylist.yview)
        self.console.rowconfigure(0, weight=1)

        self.money_manager = classes.money_manager.Money_manager(gv.current_money, gv.sell_at_high, gv.sell_at_low,
                                                                 self.mylist)

        tabControl = ttk.Notebook(self.settings)
        tabControl.grid(row=0, column=0, sticky=NSEW)
        self.settings.columnconfigure(0, weight=1)
        self.settings.rowconfigure(0, weight=1)
        self.options = Options(tabControl, controller, self.money_manager, self.console)

    def __CreateCanvas(self):
        self.canvas = FigureCanvasTkAgg(self.fig, self.graphFrame)
        self.canvas.draw()

        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=3, rowspan=3, sticky=NSEW)
        self.canvas.get_tk_widget().columnconfigure(0, weight=1)
        self.canvas.get_tk_widget().rowconfigure(0, weight=1)

    def __ClearPage(self):
        if self.animation:
            self.ani.event_source.stop()
            self.tactic = Tactics(self.ax1, self.mylist, self.options, self.money_manager)
        self.animation = True

        for item in self.canvas.get_tk_widget().find_all():
            self.canvas.get_tk_widget().delete(item)
        self.ax1.cla()

    def __DrawGraph(self, money_manager):
        self.animateButton['state'] = 'disabled'
        self.resetButton['state'] = 'normal'
        self.pause = False

        self.__ClearPage()
        self.__CreateCanvas()

        self.ani = animation.FuncAnimation(self.fig,
                                           lambda _: animate(_, self.ani, self.ax1, self.pause,
                                                             self.options,
                                                             self.tactic,
                                                             self.money_manager), interval=self.speed)



