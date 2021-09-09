import tkinter as tk
from tkinter import ttk
from globalvars import *
from tkcalendar import DateEntry
from classes.components.datamanager import *
import time


class Options:
    def __init__(self, tabControl, mylist, moneyManager, controller):
        self.mylist = mylist
        self.toAnimate = [False, False, False, False, False]
        self.toTrade = [0, 0, 0, 0]
        self.startdate = "1531216800"
        self.enddate = "1551648800"
        self.jsonObject = GetJsonData('data.json')
        self.oldCoin = self.jsonObject['coin']

        parent = Frame(tabControl)
        botSettings = Frame(tabControl)

        tabControl.add(parent, text='Graph Settings')
        tabControl.add(botSettings, text='Bot Settings')

        self.__GraphSettings(parent, moneyManager, controller)
        self.__BotSettings(botSettings, moneyManager, controller)

    def __GraphSettings(self, parent, moneyManager, controller):
        coinlabel = ttk.Label(parent, text="Change coin: ", font=normalFont)
        coinlabel.pack()

        newcoinVar = tk.StringVar()
        coin = Entry(parent, textvariable=newcoinVar)
        coin.insert(0, self.jsonObject['coin'])
        coin.pack()
        coin.bind("<Button-1>", lambda _: self.__NewPlaceholder(coin, self.jsonObject, 'coin', newcoinVar.get()))
        coin.bind("<FocusOut> ", lambda _: self.__ChangePlaceholder(coin, newcoinVar.get(), self.jsonObject['coin']))

        currencylabel = ttk.Label(parent, text="Change currency: ", font=normalFont)
        currencylabel.pack()

        newcurrencyVar = tk.StringVar()
        currency = Entry(parent, textvariable=newcurrencyVar)
        currency.insert(0, self.jsonObject['fiat'])
        currency.pack()
        currency.bind("<Button-1>",
                      lambda _: self.__NewPlaceholder(currency, self.jsonObject, 'fiat', newcurrencyVar.get()))
        currency.bind("<FocusOut> ",
                      lambda _: self.__ChangePlaceholder(currency, newcurrencyVar.get(), self.jsonObject['fiat']))
        currency.bind("<Leave> ", lambda _: self.__ChangePlaceholder(coin, newcoinVar.get(), self.jsonObject['coin']))

        startdatelabel = ttk.Label(parent, text="Change starting date: ", font=normalFont)
        startdatelabel.pack()

        startCal = MyDateEntry(parent, width=12, background='darkblue',
                               foreground='white', borderwidth=2, year=2018, month=7, day=10)
        startCal.pack(padx=10, pady=10)

        enddatelabel = ttk.Label(parent, text="Change end date: ", font=normalFont)
        enddatelabel.pack()

        endCal = MyDateEntry(parent, width=12, background='darkblue',
                             foreground='white', borderwidth=2, year=2019, month=3, day=3)
        endCal.pack(padx=10, pady=10)

        startCal.bind("<<DateEntrySelected>>", lambda _: self.__DateToEpoch(startCal, endCal))
        endCal.bind("<<DateEntrySelected>>", lambda _: self.__DateToEpoch(startCal, endCal))

        submitButton = tk.Button(parent, text='Submit',
                            command=lambda: self.Submit(newcoinVar, newcurrencyVar, moneyManager, controller))
        submitButton.pack()

        var1 = tk.IntVar()
        var2 = tk.IntVar()
        var3 = tk.IntVar()
        var4 = tk.IntVar()
        # var5 = tk.IntVar()
        c1 = Checkbutton(parent, text='MACD', variable=var1, onvalue=1, offvalue=0, command=lambda: self.SetAnimate(0))
        c1.pack(side=TOP, anchor=W)
        c2 = Checkbutton(parent, text='Bollinger Bands', variable=var2, onvalue=1, offvalue=0,
                         command=lambda: self.SetAnimate(1))
        c2.pack(side=TOP, anchor=W)
        c3 = Checkbutton(parent, text='Fibonacci retracement', variable=var3, onvalue=1, offvalue=0,
                         command=lambda: self.SetAnimate(2))
        c3.pack(side=TOP, anchor=W)
        c4 = Checkbutton(parent, text='RSI', variable=var4, onvalue=1, offvalue=0, command=lambda: self.SetAnimate(3))
        c4.pack(side=TOP, anchor=W)
        # c5 = Checkbutton(parent, text='Ichimoku cloud', variable=var5, onvalue=1, offvalue=0)
        # c5.pack(side=TOP, anchor=W)

        #CreateJsonMoney()

    def SetAnimate(self, i):
        self.toAnimate[i] = (not self.toAnimate[i])

    def __BotSettings(self, botSettings, moneyManager, controller):
        jsonObjectMoney = GetJsonData('data_money.json')

        currentMoney = ttk.Label(botSettings,
                                  text="Current money: " + str(round(float(jsonObjectMoney['current_money']), 2)),
                                  font=normalFont)
        currentMoney.pack()

        self.sellHighStrVar = tk.StringVar()
        currMonHigh = Entry(botSettings, text=self.sellHighStrVar)
        currMonHigh.insert(0, jsonObjectMoney['sell_high_val'])
        currMonHigh.pack()
        currMonHigh.bind("<Button-1>",
                           lambda _: self.__NewPlaceholder(currMonHigh, jsonObjectMoney, "sell_high",
                                                           self.sellHighStrVar.get()))
        currMonHigh.bind("<FocusOut> ",
                           lambda _: self.__ChangePlaceholder(currMonHigh, self.sellHighStrVar.get(),
                                                              jsonObjectMoney['sell_high_val']))

        self.sellLowStrVar = tk.StringVar()
        currMonLow = Entry(botSettings, text=self.sellLowStrVar)
        currMonLow.insert(0, jsonObjectMoney['sell_low_val'])
        currMonLow.pack()
        currMonLow.bind("<Button-1>",
                          lambda _: self.__NewPlaceholder(currMonLow, jsonObjectMoney, "sell_low",
                                                          self.sellLowStrVar.get()))
        currMonLow.bind("<FocusOut> ", lambda _: self.__ChangePlaceholder(currMonLow, self.sellLowStrVar.get(),
                                                                            jsonObjectMoney['sell_low_val']))

        strategy = ttk.Label(botSettings,
                             text="Investing strategy: ",
                             font=normalFont)
        strategy.pack()
        self.var = IntVar()
        self.var.set(0)
        noneRadio = Radiobutton(botSettings, text="none", variable=self.var, value=0,
                                command=lambda: self.SetTradeOption(0, moneyManager))
        noneRadio.pack(side=TOP, anchor=W)

        macdRadio = Radiobutton(botSettings, text="MACD", variable=self.var, value=1,
                                command=lambda: self.SetTradeOption(1, moneyManager))
        macdRadio.pack(side=TOP, anchor=W)

        fiboRadio = Radiobutton(botSettings, text="Fibonaci Retracement", variable=self.var, value=2,
                                command=lambda: self.SetTradeOption(2, moneyManager))
        fiboRadio.pack(side=TOP, anchor=W)
        rsiBoilingerRadio = Radiobutton(botSettings, text="Boilinger Bands & RSI", variable=self.var, value=3,
                                        command=lambda: self.SetTradeOption(3, moneyManager))
        rsiBoilingerRadio.pack(side=TOP, anchor=W)

        strategy = ttk.Label(botSettings,
                             text="Auto exit: ",
                             font=normalFont)
        strategy.pack()

        self.autoEnter = IntVar()
        self.autoEnter.set(0)
        autoEnterTrue = Radiobutton(botSettings, text="Yes", variable=self.autoEnter, value=0,
                                command=lambda: moneyManager.ChangeAutoTrade(True))
        autoEnterTrue.pack(side=TOP, anchor=W)
        autoEnterFalse = Radiobutton(botSettings, text="No", variable=self.autoEnter, value=1,
                                        command=lambda: moneyManager.ChangeAutoTrade(False))
        autoEnterFalse.pack(side=TOP, anchor=W)

    def SetTradeOption(self, i, moneyManager):
        self.ExitTrade(moneyManager)
        self.toTrade = [0, 0, 0, 0]
        self.toTrade[i] = 1

    def EnterTrade(self, moneyManager):
        justEntered = moneyManager.EnterTrade()
        if justEntered:
            text = [
                "\n Entering trade " + str(round(moneyManager.currentMoney,4))
            ]
            Log(self.mylist, text, 'green')

    def ExitTrade(self, moneyManager):
        if moneyManager.inTrading == False:
            return
        justExited = moneyManager.ExitTrade()
        if justExited:
            text = [
                "\n Exiting trade " + str(round(moneyManager.currentMoney,4))
            ]
            Log(self.mylist, text, 'red')


    def Submit(self, newcoinVar, newcurrencyVar, moneyManager, controller):
        DeleteFile('data.json')
        CreateJson(newcoinVar.get(), newcurrencyVar.get(), self.oldCoin, self.startdate,
                   self.enddate)
        sellHighCent = float(self.sellHighStrVar.get()) / float(moneyManager.currentMoney)
        sellLowCent = float(self.sellLowStrVar.get()) / float(moneyManager.currentMoney)
        CreateJsonMoney(float(moneyManager.currentMoney), sellHighCent, sellLowCent)
        moneyManager.sellLow = float(self.sellLowStrVar.get())
        moneyManager.sellHigh = float(self.sellHighStrVar.get())

        if not controller.animation:
            controller.ClearPage()
            controller.CreateCanvas()
        else:
            controller.DrawGraph()

    def __DateToEpoch(self, startCal, endCal):
        newstartdateVar = startCal.get_date()
        newenddateVar = endCal.get_date()
        pattern = '%Y-%m-%d'
        epochStart = int(time.mktime(time.strptime(str(newstartdateVar), pattern)))
        epochEnd = int(time.mktime(time.strptime(str(newenddateVar), pattern)))
        self.startdate = epochStart
        self.enddate = epochEnd

    def __NewPlaceholder(self, entry, jsonobject, ob, value):
        entry.delete(0, 'end')
        if not value == "":
            jsonobject[ob] = value

    def __ChangePlaceholder(self, entry, value, jsonObject):
        if value == "":
            entry.insert(0, jsonObject)


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
            if self.winfo_toplevel().attributes('-topmost'):
                self._top_cal.attributes('-topmost', True)
            else:
                self._top_cal.attributes('-topmost', False)
            # - patch begin: make sure the drop-down calendar is visible
            if x + self._top_cal.winfo_width() > self.winfo_screenwidth():
                x = self.winfo_screenwidth() - self._top_cal.winfo_width()
            if y + self._top_cal.winfo_height() > self.winfo_screenheight() - 30:
                y = self.winfo_rooty() - self._top_cal.winfo_height()
            # - patch end
            self._top_cal.geometry('+%i+%i' % (x, y))
            self._top_cal.deiconify()
            self._calendar.focus_set()
            self._calendar.selection_set(date)
