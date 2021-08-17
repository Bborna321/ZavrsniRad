import tkinter as tk
from tkinter import ttk
from tkinter import *
from global_vars import *
from tkcalendar import Calendar, DateEntry
from classes.components.datamanager import *
import classes.mainwindows as draw
import time
import global_vars as gv
import asyncio
import classes.components.datamanager as datamanager


def turnOnOffMacd():
    global macdOnOff
    print("jesam u ovoj funkciji")
    if macdOnOff == "off":
        macdOnOff = "on"
    elif macdOnOff == "on":
        macdOnOff = "off"


def Menubar(container):
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

    # dataTF = tk.Menu(menubar, tearoff=1)
    # dataTF.add_command(label="Tick", command=lambda: changeTimeFrame('tick'))
    # dataTF.add_command(label="1 Day", command=lambda: changeTimeFrame('1d'))
    # dataTF.add_command(label="3 Day", command=lambda: changeTimeFrame('3d'))
    # dataTF.add_command(label="1 Week", command=lambda: changeTimeFrame('7d'))
    #
    # menubar.add_cascade(label="Data Time Frame", menu=dataTF)

    macd_on_off = tk.Menu(menubar, tearoff=0)
    macd_on_off.add_command(label="Turn Macd On/Off", command=lambda: turnOnOffMacd())
    menubar.add_cascade(label="Macd", menu=macd_on_off)

    OHLCI = tk.Menu(menubar, tearoff=1)
    OHLCI.add_command(label="Tick", command=lambda: changeSampleSize('tick'))
    OHLCI.add_command(label="1 minute", command=lambda: changeSampleSize('1Min', 0.0006))
    OHLCI.add_command(label="5 minute", command=lambda: changeSampleSize('5Min', 0.003))
    OHLCI.add_command(label="15 minute", command=lambda: changeSampleSize('15Min', 0.008))
    OHLCI.add_command(label="30 minute", command=lambda: changeSampleSize('30Min', 0.016))
    OHLCI.add_command(label="1 Hour", command=lambda: changeSampleSize('1H', 0.032))
    OHLCI.add_command(label="3 Hour", command=lambda: changeSampleSize('3H', 0.096))

    menubar.add_cascade(label="OHLC Intercal", menu=OHLCI)

    topIndi = tk.Menu(menubar, tearoff=1)
    topIndi.add_command(label="None", command=lambda: addIndicator('top', 'none'))
    topIndi.add_command(label="RSI", command=lambda: addIndicator('top', 'rsi'))
    topIndi.add_command(label="MACD", command=lambda: addIndicator('top', 'macd'))

    menubar.add_cascade(label="Top indicator", menu=topIndi)

    mainI = tk.Menu(menubar, tearoff=1)
    mainI.add_command(label="None", command=lambda: addMidIndicator('none'))
    mainI.add_command(label="SMA", command=lambda: addMidIndicator('sma'))
    mainI.add_command(label="EMA", command=lambda: addMidIndicator('ema'))

    menubar.add_cascade(label="Main/middle Indicator", menu=mainI)

    bottomI = tk.Menu(menubar, tearoff=1)
    bottomI.add_command(label="None", command=lambda: addIndicator('bot', 'none'))
    bottomI.add_command(label="RST", command=lambda: addIndicator('bot', 'rsi'))
    bottomI.add_command(label="MACD", command=lambda: addIndicator('bot', 'macd'))

    menubar.add_cascade(label="Bot indicator", menu=bottomI)

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
    startStop.add_command(label="Resume", command=lambda: loadChart('start'))
    startStop.add_command(label="Stop", command=lambda: loadChart('stop'))
    menubar.add_cascade(label="Resume/Pause client", menu=startStop)

    helpMenu = tk.Menu(menubar, tearoff=0)
    helpMenu.add_command(label="Tutorial", command=tutorial)

    menubar.add_cascade(label="Help", menu=helpMenu)
    return menubar

"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""
"""TU MALO IZNAD SE PIŠE"""

# label_ljepi = tk.Label(text=jsonObjectMoney['current_money'])
# label_ljepi.configure(text=jsonObjectMoney['current_money'])
# label_ljepi.pack()

"""current_money_label = ttk.Label(parent, text="Current Money: ", font=normal_font)
current_money_label.pack()

current_money = Entry(parent, textvariable=str(gv.current_money))
current_money.insert(0, str(gv.current_money))
current_money.pack()

sell_high_label = ttk.Label(parent, text="Sell at high: ", font=normal_font)
sell_high_label.pack()

sell_high = Entry(parent, textvariable=str(gv.sell_at_high))
sell_high.insert(0, str(gv.sell_at_high))
sell_high.pack()

sell_low_label = ttk.Label(parent, text="Sell at low: ", font=normal_font)
sell_low_label.pack()

sell_low = Entry(parent, textvariable=str(gv.sell_at_low))
sell_low.insert(0, str(gv.sell_at_low))
sell_low.pack()"""


class MyDateEntry(DateEntry):
    def drop_down(self):
        """Display or withdraw the drop-down calendar depending on its current state."""
        if self._calendar.winfo_ismapped():
            self._top_cal.withdraw()
        else:
            self._validate_date()
            date = self.parse_date(self.get())
            x = self.winfo_rootx()
            y = self.winfo_rooty() + self.winfo_height()
            print(x, y)
            if self.winfo_toplevel().attributes('-topmost'):
                self._top_cal.attributes('-topmost', True)
            else:
                self._top_cal.attributes('-topmost', False)
            # - patch begin: make sure the drop-down calendar is visible
            if x + self._top_cal.winfo_width() > self.winfo_screenwidth():
                print("tu")
                x = self.winfo_screenwidth() - self._top_cal.winfo_width()
            if y + self._top_cal.winfo_height() > self.winfo_screenheight() - 30:
                print("tamo")
                y = self.winfo_rooty() - self._top_cal.winfo_height()
            # - patch end
            self._top_cal.geometry('+%i+%i' % (x, y))
            self._top_cal.deiconify()
            self._calendar.focus_set()
            self._calendar.selection_set(date)

"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""
"""NE GLEDAT ISPOD"""


def addIndicator(where, what):
    if dataPace == 'tick':
        popupmsg("Indicators in tick not available")
    elif what == "none":
        if where == "top":
            topIndicator = what
        elif where == "bot":
            botIndicator = what
        DatCounter = 9000
    elif what == 'rsi':
        rsiQ = tk.Tk()
        rsiQ.wm_title("Periods?")
        label = ttk.Label(rsiQ, text="How many day for RSI?")
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(rsiQ)
        e.insert(0, 14)
        e.pack()
        e.focus_set()

        def callback():
            global topIndicator
            global botIndicator
            global DatCounter

            periods = (e.get())
            group = ["rsi", periods]
            DatCounter = 9000
            if where == "top":
                topIndicator = what
                print("Set top indicator:", group)
            elif where == "bot":
                botIndicator = what
                print("Set bot indicator:", group)
            rsiQ.destroy()

        b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
        b.pack()
        tk.mainloop()

    elif what == "macd":
        DatCounter = 9000
        if where == "top":
            topIndicator = what
            print("Set top indicator:", what)
        elif where == "bot":
            botIndicator = what
            print("Set bot indicator:", what)


def ReplacePeriods():
    midIQ = tk.Tk()
    midIQ.wm_title("Periods?")
    label = ttk.Label(midIQ, text="Choose how many periods: ")
    label.pack(side="top", fill="x", pady=10)
    e = ttk.Entry(midIQ)
    e.insert(0, 10)
    e.pack()
    e.focus_set()
    return midIQ


def addMidIndicator(what):
    global midIndicator
    if dataPace == "Tick":
        popupmsg("Indicators in Tick Data not available")

    if what != "none":
        if midIndicator == "none":
            if what == "sma":
                midIQ = ReplacePeriods()

                def callback():
                    global midIndicator
                    global DatCounter
                    midIndicator = []
                    periods = (e.get())
                    group = ["sma", int(periods)]
                    midIndicator.append(group)
                    DatCounter = 9000
                    print("middle indicator set to: ", midIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()
            elif what == "ema":
                midIQ = ReplacePeriods()

                def callback():
                    global midIndicator
                    global DatCounter
                    midIndicator = []
                    periods = (e.get())
                    group = ["ema", int(periods)]
                    midIndicator.append(group)
                    DatCounter = 9000
                    print("middle indicator set to: ", midIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()
            else:
                if what == "sma":
                    midIQ = tk.Tk()
                    midIQ.wm_title("Periods?")
                    label = ttk.Label(midIQ, text="Choose how many periods: ")
                    label.pack()(side="top", fill="x", pady=10)
                    e = ttk.Entry(midIQ)
                    e.insert(0, 10)
                    e.pack()
                    e.focus_set()

                    def callback():
                        global midIndicator
                        global DatCounter
                        periods = (e.get())
                        group = ["sma", int(periods)]
                        midIndicator.append(group)
                        DatCounter = 9000
                        print("middle indicator set to: ", midIndicator)
                        midIQ.destroy()

                    b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                    b.pack()
                    tk.mainloop()
                elif what == "ema":
                    midIQ = ReplacePeriods()

                    def callback():
                        global midIndicator
                        global DatCounter
                        periods = (e.get())
                        group = ["ema", int(periods)]
                        midIndicator.append(group)
                        DatCounter = 9000
                        print("middle indicator set to: ", midIndicator)
                        midIQ.destroy()

                    b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                    b.pack()
                    tk.mainloop()
    else:
        midIndicator = "none"


def loadChart(run):
    global chartLoad

    if run == "start":
        chartLoad = True
    elif run == "stop":
        chartLoad = False


def tutorial():
    pass


def changeTimeFrame(tf):
    global dataPace
    global DatCounter
    if tf == "7d" and resampleSize == "1Min":
        popupmsg("Too much data chosen")
    else:
        dataPace = tf
        DatCounter = 9000


def changeSampleSize(size, width):
    global resampleSize
    global DatCounter
    global candleWidth
    if dataPace == "7d" and resampleSize == "1Min":
        popupmsg("Too much data chosen")
    elif dataPace == "thick":
        popupmsg("You are on tick data, ont OHLC")
    else:
        resampleSize = size
        DatCounter = 9000
        candleWidth = width


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
    B1 = ttk.Button(popup, text="Stop", command=leavemini)
    B1.pack()
    B2 = ttk.Button(popup, text="Resume", command=leavemini)
    B2.pack()
    popup.mainloop()
