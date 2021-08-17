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





startdate = "1531216800"
enddate = "1551648800"


class Options:
    def __init__(self, tabControl, controller, money_manager):
        self.toAnimate = [0, 0, 0, 0, 0]
        global startdate
        global enddate
        jsonObject = GetJsonData()
        oldCoin = jsonObject['coin']

        parent = Frame(tabControl)
        botSettings = Frame(tabControl)

        tabControl.add(parent, text='Graph Settings')
        tabControl.add(botSettings, text='Bot Settings')

        def newPlaceholder(entry, jsonobject, ob, value):
            entry.delete(0, 'end')
            print(value)
            if not value == "":
                jsonobject[ob] = value

        def ChangePlaceholder(entry, value, jsonObject):
            print(value)
            if value == "":
                entry.insert(0, jsonObject)

        def ChangePlaceholderMoney(entry, value, jsonObject):
            try:
                entry.insert(0, jsonObject)
            except Exception:
                print("ne meže, sori",Exception)



            # controller.show_frame(GraphPage)

        coinlabel = ttk.Label(parent, text="Change coin: ", font=normal_font)
        coinlabel.pack()

        newcoin_var = tk.StringVar()
        coin = Entry(parent, textvariable=newcoin_var)
        coin.insert(0, jsonObject['coin'])
        coin.pack()
        coin.bind("<Button-1>", lambda _: newPlaceholder(coin, jsonObject, 'coin', newcoin_var.get()))
        coin.bind("<FocusOut> ", lambda _: ChangePlaceholder(coin, newcoin_var.get(), jsonObject['coin']))



        currencylabel = ttk.Label(parent, text="Change currency: ", font=normal_font)
        currencylabel.pack()

        newcurrency_var = tk.StringVar()
        currency = Entry(parent, textvariable=newcurrency_var)
        currency.insert(0, jsonObject['fiat'])
        currency.pack()
        currency.bind("<Button-1>", lambda _: newPlaceholder(currency, jsonObject, 'fiat', newcurrency_var.get()))
        currency.bind("<FocusOut> ", lambda _: ChangePlaceholder(currency, newcurrency_var.get(), jsonObject['fiat']))
        currency.bind("<Leave> ", lambda _: ChangePlaceholder(coin, newcoin_var.get(), jsonObject['coin']))

        def print_sel():
            global startdate
            global enddate
            newstartdate_var = startCal.get_date()
            newenddate_var = endCal.get_date()
            pattern = '%Y-%m-%d'
            epochStart = int(time.mktime(time.strptime(str(newstartdate_var), pattern)))
            epochEnd = int(time.mktime(time.strptime(str(newenddate_var), pattern)))
            startdate = epochStart
            enddate = epochEnd

        startdatelabel = ttk.Label(parent, text="Change starting date: ", font=normal_font)
        startdatelabel.pack()

        startCal = MyDateEntry(parent, width=12, background='darkblue',
                               foreground='white', borderwidth=2, year=2018, month=7, day=10)
        startCal.pack(padx=10, pady=10)
        startCal.bind("<<DateEntrySelected>>", lambda _: print_sel())

        enddatelabel = ttk.Label(parent, text="Change end date: ", font=normal_font)
        enddatelabel.pack()

        endCal = MyDateEntry(parent, width=12, background='darkblue',
                             foreground='white', borderwidth=2, year=2019, month=3, day=3)
        endCal.pack(padx=10, pady=10)
        endCal.bind("<<DateEntrySelected>>", lambda _: print_sel())

        var1 = tk.IntVar()
        var2 = tk.IntVar()
        var3 = tk.IntVar()
        var4 = tk.IntVar()
        # var5 = tk.IntVar()
        c1 = Checkbutton(parent, text='MACD', variable=var1, onvalue=1, offvalue=0)
        c1.pack(side=TOP, anchor=W)
        c2 = Checkbutton(parent, text='Bollinger Bands', variable=var2, onvalue=1, offvalue=0)
        c2.pack(side=TOP, anchor=W)
        c3 = Checkbutton(parent, text='Fibonacci retracement', variable=var3, onvalue=1, offvalue=0)
        c3.pack(side=TOP, anchor=W)
        c4 = Checkbutton(parent, text='RSI', variable=var4, onvalue=1, offvalue=0)
        c4.pack(side=TOP, anchor=W)
        # c5 = Checkbutton(parent, text='Ichimoku cloud', variable=var5, onvalue=1, offvalue=0)
        # c5.pack(side=TOP, anchor=W)

        """newcoin_var = tk.StringVar()
        coin = Entry(parent, textvariable=newcoin_var)
        coin.insert(0, jsonObject['coin'])
        coin.pack()"""

        def Submit():
            self.toAnimate = [var1.get(), var2.get(), var3.get(), var4.get(), 0]
            print(self.toAnimate)
            CreateJson(newcoin_var.get(), newcurrency_var.get(), oldCoin, startdate,
                       enddate)
            #CreateJsonMoney(current_money=current_money_str_var.get())

        sub_btn = tk.Button(parent, text='Submit', command=Submit)
        sub_btn.pack()

        jsonObjectMoney = GetJsonDataMoney()

        """label = tk.Label(text="")
        label.configure(text=gv.current_money)
        label.pack()"""

        current_money_str_var = tk.StringVar()
        curr_mon = Entry(botSettings, text=current_money_str_var)
        curr_mon.insert(0, jsonObjectMoney['current_money'])
        curr_mon.pack()
        curr_mon.bind("<Button-1>",
                      lambda _: newPlaceholder(curr_mon, jsonObjectMoney, "current_money", current_money_str_var.get()))
        curr_mon.bind("<FocusOut> ", lambda _: ChangePlaceholder(curr_mon, current_money_str_var.get(),
                                                                 jsonObjectMoney['current_money']))


        start_tradeing_btn = tk.Button(botSettings, text='Enter Trade', command=lambda :self.enter_trade(money_manager))
        start_tradeing_btn.pack()

        stop_tradeing_btn = tk.Button(botSettings, text='Exit Trade', command=lambda: self.exit_trade(money_manager))
        stop_tradeing_btn.pack()
    def enter_trade(self,money_manager):
        money_manager.in_trading = True
        money_manager.sell_low = money_manager.current_money*0.84
        money_manager.sell_high = money_manager.current_money * 1.2
        print("u enteru sam")

    def exit_trade(self,money_manager):
        money_manager.in_trading = False
        print("u exitu sam")

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

        #label_ljepi = tk.Label(text=jsonObjectMoney['current_money'])
        #label_ljepi.configure(text=jsonObjectMoney['current_money'])
        #label_ljepi.pack()



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