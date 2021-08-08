# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib import style
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.figure import Figure
from mplfinance.original_flavor import candlestick_ohlc
import finplot as fplt
import mplfinance as mpf
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib import  pyplot as plt
import matplotlib.animation as animation
from scipy.interpolate import make_interp_spline
import numpy as np
#import tkinter_Windows as tWin
import global_vars as gv
import historical_data as hsd

import urllib
import json

import pandas as pd

large_font=('Verdana',12)
normal_font=('Verdana',10)
small_font=('Verdana',8)
style.use('ggplot')

darkColor = "#892020"
lightColor = "#208989"
lightColor_prev = "#7fff00"

f = Figure(figsize=(21,9), dpi=90)
#f = Figure()
a = f.add_subplot(111)

exchange = "BTC-e"
DatCounter = 9000
programName = "coinbase"

resampleSize = "15Min"
dataPace="tick"
candleWidth = 0.008
paneCount=1

topIndicator="none"
botIndicator="none"
midIndicator="none"
EMAs=[]
SMAs=[]
chartLoad=True

def addIndicator(where,what):
    global topIndicator
    global botIndicator
    global DatCounter

    if dataPace == 'tick':
        popupmsg("Indicators in tick not available")
    elif what=="none":
        if where=="top":
            topIndicator=what
        elif where=="bot":
            botIndicator=what
        DatCounter=9000
    elif what=='rsi':
        rsiQ = tk.Tk()
        rsiQ.wm_title("Periods?")
        label = ttk.Label(rsiQ,text="How many day for RSI?")
        label.pack(side="top", fill="x",pady=10)

        e = ttk.Entry(rsiQ)
        e.insert(0,14)
        e.pack()
        e.focus_set()

        def callback():
            global topIndicator
            global botIndicator
            global DatCounter

            periods =(e.get())
            group = []
            group.append(("rsi"))
            group.append(periods)


            DatCounter=9000
            if where == "top":
                topIndicator = what
                print("Set top indicator:", group)
            elif where == "bot":
                botIndicator = what
                print("Set bot indicator:", group)
            rsiQ.destroy()

        b=ttk.Button(rsiQ,text="Submit",width=10,command=callback)
        b.pack()
        tk.mainloop()

    elif what == "macd":
        DatCounter = 9000
        if where=="top":
            topIndicator=what
            print("Set top indicator:", what)
        elif where=="bot":
            botIndicator=what
            print("Set bot indicator:", what)

def addMidIndicator(what):
    global midIndicator
    global DatCounter

    if dataPace=="Tick":
        popupmsg("Indicators in Tick Data not available")

    if what!="none":
        if midIndicator=="none":
            if what=="sma":
                midIQ=tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods: ")
                label.pack(side="top",fill="x",pady=10)
                e=ttk.Entry(midIQ)
                e.insert(0,10)
                e.pack()
                e.focus_set()

                def callback():
                    global midIndicator
                    global DatCounter
                    midIndicator=[]
                    periods=(e.get())
                    group=[]
                    group.append("sma")
                    group.append(int(periods))
                    midIndicator.append(group)
                    DatCounter = 9000
                    print("middle indicator set to: ",midIndicator)
                    midIQ.destroy()
                b = ttk.Button(midIQ,text="Submit",width=10,command=callback)
                b.pack()
                tk.mainloop()
            elif what=="ema":
                midIQ=tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods: ")
                label.pack(side="top",fill="x",pady=10)
                e=ttk.Entry(midIQ)
                e.insert(0,10)
                e.pack()
                e.focus_set()

                def callback():
                    global midIndicator
                    global DatCounter
                    midIndicator=[]
                    periods=(e.get())
                    group=[]
                    group.append("ema")
                    group.append(int(periods))
                    midIndicator.append(group)
                    DatCounter = 9000
                    print("middle indicator set to: ",midIndicator)
                    midIQ.destroy()
                b = ttk.Button(midIQ,text="Submit",width=10,command=callback)
                b.pack()
                tk.mainloop()
            else:
                if what=="sma":
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
                        group = []
                        group.append("sma")
                        group.append(int(periods))
                        midIndicator.append(group)
                        DatCounter = 9000
                        print("middle indicator set to: ", midIndicator)
                        midIQ.destroy()

                    b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                    b.pack()
                    tk.mainloop()
                elif what=="ema":
                    midIQ = tk.Tk()
                    midIQ.wm_title("Periods?")
                    label = ttk.Label(midIQ, text="Choose how many periods: ")
                    label.pack(side="top", fill="x", pady=10)
                    e = ttk.Entry(midIQ)
                    e.insert(0, 10)
                    e.pack()
                    e.focus_set()

                    def callback():
                        global midIndicator
                        global DatCounter
                        periods = (e.get())
                        group = []
                        group.append("ema")
                        group.append(int(periods))
                        midIndicator.append(group)
                        DatCounter = 9000
                        print("middle indicator set to: ", midIndicator)
                        midIQ.destroy()

                    b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                    b.pack()
                    tk.mainloop()
    else:
        midIndicator="none"


def loadChart(run):
    global charLoad

    if run=="start":
        chartLoad=True
    elif run=="stop":
        chartLoad=False

def tutorial():
    pass

def changeTimeFrame(tf):
    global dataPace
    global DatCounter
    if tf == "7d" and resampleSize =="1Min":
        popupmsg("Too much data chosen")
    else:
        dataPace=tf
        DatCounter=9000


def changeSampleSize(size,width):
    global resampleSize
    global DatCounter
    global candleWidth
    if dataPace == "7d" and resampleSize =="1Min":
        popupmsg("Too much data chosen")
    elif dataPace == "thick":
        popupmsg("You are on tick data, ont OHLC")
    else:
        resampleSize = size
        DatCounter = 9000
        candleWidth = width

def changeExchange(toWhat,pn):
    global exchange
    global DatCounter
    global programName

    exchange = toWhat
    programName = pn
    DatCounter

def animate(i):

    pullData = open('sampleData.txt','r').read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            xl,yl = eachLine.split(',')
            xList.append(int(xl))
            yList.append(int(yl))

    a.clear()
    x=xList
    y=yList
    X_Y_Spline = make_interp_spline(x, y)

    # Returns evenly spaced numbers
    # over a specified interval.
    X_ = np.linspace(min(x), max(x), 220)
    Y_ = X_Y_Spline(X_)
    a.plot(X_, Y_)

def animate_real_deal(y):
    global refreshRate
    global DatCounter
    global firstLoadOfGraph
    ani.pause()
    if chartLoad:
        if paneCount == 1:
            if dataPace=="tick":
                try:

                    #a = plt.subplot2grid((6,2),(0,0),rowspan=5,colspan=4)
                    #print(a)
                    #a2 = plt.subplot2grid((6,2),(5,0),rowspan=1,colspan=4,sharex=a)

                    data = hsd.cbpGetHistoricRates(gv.market, granularity=gv.granularity)
                    #data_ohlc = hsd.

                    a.clear()

                    a.set_xlabel('Date')
                    a.set_ylabel('Price')


                    """jedan koristi ohlc a jedan ohcl!!! ....."""


                    #candlestick_ohlc(a,data.values(),width=2,colordown=darkColor,colorup=lightColor)

                    df = pd.DataFrame(data.values(), columns='time open high low close'.split())
                    fplt.candlestick_ochl(df[['time', 'open', 'close', 'high', 'low']],a)

                    #a.plot_date(dates_plot, values_plot_close, darkColor, label='close')
                    #a.plot_date(dates_plot,values_plot_open,lightColor,label='open')
                    a.xaxis.set_major_locator(mticker.MaxNLocator(11))
                    a.grid(True)
                    #date_format = mdates.DateFormatter('%Y-%m-%d')
                    #print(date_format)
                    #a.xaxis.set_major_formatter(date_format)

                    #a.legend(bbox_to_anchor=(0,1.02,1,.102),loc=4,ncol=2,borderaxespad=0)
                    last_price=''
                    for vals in data.values().__reversed__():
                        last_price=str(vals[-1])

                    title = gv.market.split('-')[0] +' historical data\nLast price: '+last_price+' '+ gv.market.split('-')[1]
                    a.set_title(title)
                except Exception as e:
                    print("Failed because of:",e)
            fplt.show()

def popupmsg(msg):
    popup = tk.Tk()

    def leavemini():
        popup.destroy()

    popup.wm_title("!!!")
    label=ttk.Label(popup, text=msg, font=normal_font)
    label.pack(side="top",fill="x",pady=10 )
    B1 = ttk.Button(popup,text="OK",command=leavemini)
    B1.pack()
    popup.mainloop()

class Window_tkinter(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)

        #tk.Tk.iconbitmap(self,default='@./mario.xbm')
        tk.Tk.wm_title(self, "Bot 'n' stuff")

        container = tk.Frame(self)
        container.pack( side='top', fill='both', expand=True )
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        #filemenu.add_command(label="Save settings", command=lambda:tk.messagebox.showinfo(' ',"Not supported just yet!"))
        filemenu.add_command(label="Save settings",command=lambda: popupmsg("Not supported yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        exchangeChoice = tk.Menu(menubar,tearoff=1)

        exchangeChoice.add_command(label="Coinbase",command=lambda :changeExchange("Coinbase","Coinbase"))
        exchangeChoice.add_command(label="Bitfinex", command=lambda: changeExchange("Bitfinix", "bitfinex"))
        exchangeChoice.add_command(label="Bitstamp", command=lambda: changeExchange("Bitstamp", "bitstamp"))
        exchangeChoice.add_command(label="Huobi", command=lambda: changeExchange("Huobi", "huobi"))

        menubar.add_cascade(label="Exchange", menu=exchangeChoice)


        dataTF = tk.Menu(menubar,tearoff=1)
        dataTF.add_command(label="Tick", command=lambda :changeTimeFrame('tick'))
        dataTF.add_command(label="1 Day", command=lambda: changeTimeFrame('1d'))
        dataTF.add_command(label="3 Day", command=lambda: changeTimeFrame('3d'))
        dataTF.add_command(label="1 Week", command=lambda: changeTimeFrame('7d'))

        menubar.add_cascade(label="Data Time Frame", menu = dataTF)
        OHLCI = tk.Menu(menubar, tearoff=1)
        OHLCI.add_command(label="Tick", command=lambda :changeSampleSize('tick'))
        OHLCI.add_command(label="1 minute", command=lambda: changeSampleSize('1Min',0.0006))
        OHLCI.add_command(label="5 minute", command=lambda: changeSampleSize('5Min', 0.003))
        OHLCI.add_command(label="15 minute", command=lambda: changeSampleSize('15Min', 0.008))
        OHLCI.add_command(label="30 minute", command=lambda: changeSampleSize('30Min', 0.016))
        OHLCI.add_command(label="1 Hour", command=lambda: changeSampleSize('1H', 0.0032))
        OHLCI.add_command(label="3 Hour", command=lambda: changeSampleSize('3H', 0.0096))

        menubar.add_cascade(label="OHLC Intercal", menu=OHLCI)


        topIndi = tk.Menu(menubar, tearoff=1)
        topIndi.add_command(label="None", command=lambda: addIndicator('top','none'))
        topIndi.add_command(label="RSI", command=lambda: addIndicator('top','rsi'))
        topIndi.add_command(label="MACD", command=lambda: addIndicator('top','macd'))

        menubar.add_cascade(label="Top indicator", menu=topIndi)

        mainI = tk.Menu(menubar, tearoff=1)
        mainI.add_command(label="None", command=lambda: addMidIndicator('none'))
        mainI.add_command(label="SMA", command=lambda: addMidIndicator('sma'))
        mainI.add_command(label="EMA", command=lambda: addMidIndicator('ema'))

        menubar.add_cascade(label="Main/middle Indicator", menu=mainI)

        bottomI = tk.Menu(menubar, tearoff=1)
        bottomI.add_command(label="None", command=lambda: addIndicator('bot','none'))
        bottomI.add_command(label="RST", command=lambda: addIndicator('bot','rsi'))
        bottomI.add_command(label="MACD", command=lambda: addIndicator('bot','macd'))

        menubar.add_cascade(label="Bot indicator", menu=bottomI)


        tradeButton = tk.Menu(menubar,tearoff=1)
        tradeButton.add_command(label="Manual Trading",command=lambda :popupmsg("This is not live"))
        tradeButton.add_command(label="Automated Trading", command=lambda: popupmsg("This is not live"))
        tradeButton.add_separator()
        tradeButton.add_command(label="Quick Buy",command=lambda :popupmsg("Not live"))
        tradeButton.add_command(label="Quick Sell", command=lambda: popupmsg("Not live"))

        tradeButton.add_separator()
        tradeButton.add_command(label="Set-up Quick buy/sell", command=lambda: popupmsg("Definitley not available"))

        menubar.add_cascade(label="Trading", menu=tradeButton)

        startStop = tk.Menu(menubar, tearoff=1)
        startStop.add_command(label="Resume",command=lambda :loadChart('start'))
        startStop.add_command(label="Stop", command=lambda: loadChart('stop'))
        menubar.add_cascade(label="Resume/Pause client", menu=startStop)

        helpMenu = tk.Menu(menubar,tearoff=0)
        helpMenu.add_command(label="Tutorial",command=tutorial)

        menubar.add_cascade(label="Help",menu=helpMenu)




        tk.Tk.config(self,menu=menubar)

        self.frames = {}

        for f in (FirstPage,SettingsPage,GraphPage):

            frame = f(container,self)
            self.frames[f] = frame
            frame.grid(row=0,column=0,sticky='news')
        self.show_frame(GraphPage)

    def show_frame( self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class FirstPage(tk.Frame):
    def __init__( self, parent, controller):
        tk.Frame.__init__(self, parent)
        label0 = tk.Label(self, text='Litecoin trading application', font=large_font)
        label0.pack(pady=25,padx=25)

        button0 = ttk.Button(self,text="Agree",
                           command=lambda:controller.show_frame(GraphPage))
        button0.pack()
        button02 = ttk.Button(self, text="Disagree",
                              command=lambda: quit())
        button02.pack()

class SettingsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label1 =tk.Label(self, text='Page One', font=large_font)
        label1.pack(pady=25, padx=25)
        #label11 = tk.Label(self, text='Description')
        #label11 .pack()

        button1 = ttk.Button(self,text="Confirm",
                           command=lambda: controller.show_frame(FirstPage))
        button2 = ttk.Button(self, text="Revert",
                             command=lambda: controller.show_frame(FirstPage))
        button1.pack()
        button2.pack()

class GraphPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
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

        canvas = FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        button4 = tk.Button(self,text="draw graph",command=lambda :1+1)
        button4.pack()




if __name__ == '__main__':
    win = Window_tkinter()
    win.geometry('1580x850')
    ani = animation.FuncAnimation(f, animate_real_deal, interval=2400)
    win.mainloop()





