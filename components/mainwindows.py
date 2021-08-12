from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
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
    gv.chartLoad = True


def turnOnBollingerBand():
    if gv.BollingerOnOff=="off":
        gv.BollingerOnOff = "on"
        gv.macdOnOff = "off"
    elif gv.BollingerOnOff=="on":
        gv.BollingerOnOff="off"
    gv.chartLoad = True

def drawGraph():
    gv.chartLoad=True


class Window_tkinter(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self,default='@./mario.xbm')
        tk.Tk.wm_title(self, "Bot 'n' stuff")

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        # filemenu.add_command(label="Save settings", command=lambda:tk.messagebox.showinfo(' ',"Not supported just yet!"))
        filemenu.add_command(label="Save settings", command=lambda: popupmsg("Not supported yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        exchangeChoice = tk.Menu(menubar, tearoff=1)

        exchangeChoice.add_command(label="Coinbase", command=lambda: changeExchange("Coinbase", "Coinbase"))
        exchangeChoice.add_command(label="Bitfinex", command=lambda: changeExchange("Bitfinix", "bitfinex"))
        exchangeChoice.add_command(label="Bitstamp", command=lambda: changeExchange("Bitstamp", "bitstamp"))
        exchangeChoice.add_command(label="Huobi", command=lambda: changeExchange("Huobi", "huobi"))

        menubar.add_cascade(label="Exchange", menu=exchangeChoice)

        """dataTF = tk.Menu(menubar, tearoff=1)
        dataTF.add_command(label="Tick", command=lambda: changeTimeFrame('tick'))
        dataTF.add_command(label="1 Day", command=lambda: changeTimeFrame('1d'))
        dataTF.add_command(label="3 Day", command=lambda: changeTimeFrame('3d'))
        dataTF.add_command(label="1 Week", command=lambda: changeTimeFrame('7d'))

        menubar.add_cascade(label="Data Time Frame", menu=dataTF)"""

        TradingMethods = tk.Menu(menubar,tearoff=0)
        TradingMethods.add_command(label="Turn Macd On/Off", command=lambda :turnOnOffMacd())
        TradingMethods.add_command(label="Turn Bollinger On/Off", command=lambda: turnOnBollingerBand())
        menubar.add_cascade(label="Trading Methods", menu=TradingMethods)




        tradeButton = tk.Menu(menubar, tearoff=1)
        tradeButton.add_command(label="Manual Trading", command=lambda: popupmsg("This is not live"))
        tradeButton.add_command(label="Automated Trading", command=lambda: popupmsg("This is not live"))
        tradeButton.add_separator()
        tradeButton.add_command(label="Quick Buy", command=lambda: popupmsg("Not live"))
        tradeButton.add_command(label="Quick Sell", command=lambda: popupmsg("Not live"))

        tradeButton.add_separator()
        tradeButton.add_command(label="Set-up Quick buy/sell", command=lambda: popupmsg("Definitley not available"))

        menubar.add_cascade(label="Trading", menu=tradeButton)

        startStop = tk.Menu(menubar, tearoff=1)
        startStop.add_command(label="Resume", command=lambda: 1+1 )
        startStop.add_command(label="Stop", command=lambda: 1+1)
        menubar.add_cascade(label="Resume/Pause client", menu=startStop)


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

        button4 = tk.Button(self, text="draw graph", command=lambda:drawGraph())
        button4.pack()

        def what_method_is_on():
            if gv.macdOnOff == "on":
                return "Macd is On"
            elif gv.BollingerOnOff=="on":
                return "Bollinger is On"
            else:
                return "No method is On"

        label4 = tk.Label(self, textvariable=what_method_is_on)
        label4.pack()




def changeExchange(toWhat, pn):
    global exchange
    global DatCounter
    global programName

    exchange = toWhat
    programName = pn
    DatCounter


def popupmsg(msg):
    popup = tk.Tk()

    def leavemini():
        popup.destroy()

    popup.wm_title("!!!")
    label = ttk.Label(popup, text=msg, font=normal_font)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="OK", command=leavemini)
    B1.pack()
    popup.mainloop()
