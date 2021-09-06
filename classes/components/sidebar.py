import tkinter as tk
from tkinter import ttk
from global_vars import *
from tkcalendar import DateEntry
from classes.components.datamanager import *
import time


class Options:
    def __init__(self, tabControl, mylist, money_manager, controller):
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

        self.__GraphSettings(parent, money_manager, controller)
        self.__BotSettings(botSettings, money_manager, controller)

    def __GraphSettings(self, parent, money_manager, controller):
        coinlabel = ttk.Label(parent, text="Change coin: ", font=normal_font)
        coinlabel.pack()

        newcoin_var = tk.StringVar()
        coin = Entry(parent, textvariable=newcoin_var)
        coin.insert(0, self.jsonObject['coin'])
        coin.pack()
        coin.bind("<Button-1>", lambda _: self.__NewPlaceholder(coin, self.jsonObject, 'coin', newcoin_var.get()))
        coin.bind("<FocusOut> ", lambda _: self.__ChangePlaceholder(coin, newcoin_var.get(), self.jsonObject['coin']))

        currencylabel = ttk.Label(parent, text="Change currency: ", font=normal_font)
        currencylabel.pack()

        newcurrency_var = tk.StringVar()
        currency = Entry(parent, textvariable=newcurrency_var)
        currency.insert(0, self.jsonObject['fiat'])
        currency.pack()
        currency.bind("<Button-1>",
                      lambda _: self.__NewPlaceholder(currency, self.jsonObject, 'fiat', newcurrency_var.get()))
        currency.bind("<FocusOut> ",
                      lambda _: self.__ChangePlaceholder(currency, newcurrency_var.get(), self.jsonObject['fiat']))
        currency.bind("<Leave> ", lambda _: self.__ChangePlaceholder(coin, newcoin_var.get(), self.jsonObject['coin']))

        startdatelabel = ttk.Label(parent, text="Change starting date: ", font=normal_font)
        startdatelabel.pack()

        startCal = MyDateEntry(parent, width=12, background='darkblue',
                               foreground='white', borderwidth=2, year=2018, month=7, day=10)
        startCal.pack(padx=10, pady=10)

        enddatelabel = ttk.Label(parent, text="Change end date: ", font=normal_font)
        enddatelabel.pack()

        endCal = MyDateEntry(parent, width=12, background='darkblue',
                             foreground='white', borderwidth=2, year=2019, month=3, day=3)
        endCal.pack(padx=10, pady=10)

        startCal.bind("<<DateEntrySelected>>", lambda _: self.__DateToEpoch(startCal, endCal))
        endCal.bind("<<DateEntrySelected>>", lambda _: self.__DateToEpoch(startCal, endCal))

        sub_btn = tk.Button(parent, text='Submit',
                            command=lambda: self.Submit(newcoin_var, newcurrency_var, money_manager, controller))
        sub_btn.pack()

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

    def __BotSettings(self, botSettings, money_manager, controller):
        jsonObjectMoney = GetJsonData('data_money.json')

        current_money = ttk.Label(botSettings,
                                  text="Current money: " + str(round(float(jsonObjectMoney['current_money']), 2)),
                                  font=normal_font)
        current_money.pack()

        self.sell_high_str_var = tk.StringVar()
        curr_mon_high = Entry(botSettings, text=self.sell_high_str_var)
        curr_mon_high.insert(0, jsonObjectMoney['sell_high_val'])
        curr_mon_high.pack()
        curr_mon_high.bind("<Button-1>",
                           lambda _: self.__NewPlaceholder(curr_mon_high, jsonObjectMoney, "sell_high",
                                                           self.sell_high_str_var.get()))
        curr_mon_high.bind("<FocusOut> ",
                           lambda _: self.__ChangePlaceholder(curr_mon_high, self.sell_high_str_var.get(),
                                                              jsonObjectMoney['sell_high_val']))

        self.sell_low_str_var = tk.StringVar()
        curr_mon_low = Entry(botSettings, text=self.sell_low_str_var)
        curr_mon_low.insert(0, jsonObjectMoney['sell_low_val'])
        curr_mon_low.pack()
        curr_mon_low.bind("<Button-1>",
                          lambda _: self.__NewPlaceholder(curr_mon_low, jsonObjectMoney, "sell_low",
                                                          self.sell_low_str_var.get()))
        curr_mon_low.bind("<FocusOut> ", lambda _: self.__ChangePlaceholder(curr_mon_low, self.sell_low_str_var.get(),
                                                                            jsonObjectMoney['sell_low_val']))

        strategy = ttk.Label(botSettings,
                             text="Investing strategy: ",
                             font=normal_font)
        strategy.pack()
        self.var = IntVar()
        self.var.set(0)
        noneRadio = Radiobutton(botSettings, text="none", variable=self.var, value=0,
                                command=lambda: self.SetTradeOption(0, money_manager))
        noneRadio.pack(side=TOP, anchor=W)

        macdRadio = Radiobutton(botSettings, text="MACD", variable=self.var, value=1,
                                command=lambda: self.SetTradeOption(1, money_manager))
        macdRadio.pack(side=TOP, anchor=W)

        fiboRadio = Radiobutton(botSettings, text="Fibonaci Retracement", variable=self.var, value=2,
                                command=lambda: self.SetTradeOption(2, money_manager))
        fiboRadio.pack(side=TOP, anchor=W)
        rsiBoilingerRadio = Radiobutton(botSettings, text="Boilinger Bands & RSI", variable=self.var, value=3,
                                        command=lambda: self.SetTradeOption(3, money_manager))
        rsiBoilingerRadio.pack(side=TOP, anchor=W)

        strategy = ttk.Label(botSettings,
                             text="Auto exit: ",
                             font=normal_font)
        strategy.pack()

        self.autoEnter = IntVar()
        self.autoEnter.set(0)
        autoEnterTrue = Radiobutton(botSettings, text="Yes", variable=self.autoEnter, value=0,
                                command=lambda: money_manager.ChangeAutoTrade(True))
        autoEnterTrue.pack(side=TOP, anchor=W)
        autoEnterFalse = Radiobutton(botSettings, text="No", variable=self.autoEnter, value=1,
                                        command=lambda: money_manager.ChangeAutoTrade(False))
        autoEnterFalse.pack(side=TOP, anchor=W)

    def SetTradeOption(self, i, money_manager):
        self.exit_trade(money_manager)
        self.toTrade = [0, 0, 0, 0]
        self.toTrade[i] = 1

    def enter_trade(self, money_manager):
        just_entered = money_manager.enter_trade()
        if just_entered:
            text = [
                "\n Entering trade " + str(round(money_manager.current_money,4))
            ]
            Log(self.mylist, text, 'green')

    def exit_trade(self, money_manager):
        if money_manager.in_trading == False:
            return
        just_exited = money_manager.exit_trade()
        if just_exited:
            text = [
                "\n Exiting trade " + str(round(money_manager.current_money,4))
            ]
            Log(self.mylist, text, 'red')


    def Submit(self, newcoin_var, newcurrency_var, money_manager, controller):
        DeleteFile('data.json')
        CreateJson(newcoin_var.get(), newcurrency_var.get(), self.oldCoin, self.startdate,
                   self.enddate)
        sell_high_cent = float(self.sell_high_str_var.get()) / float(money_manager.current_money)
        sell_low_cent = float(self.sell_low_str_var.get()) / float(money_manager.current_money)
        CreateJsonMoney(float(money_manager.current_money), sell_high_cent, sell_low_cent)
        money_manager.sell_low = float(self.sell_low_str_var.get())
        money_manager.sell_high = float(self.sell_high_str_var.get())

        if not controller.animation:
            controller.ClearPage()
            controller.CreateCanvas()
        else:
            controller.DrawGraph()

    def __DateToEpoch(self, startCal, endCal):
        newstartdate_var = startCal.get_date()
        newenddate_var = endCal.get_date()
        pattern = '%Y-%m-%d'
        epochStart = int(time.mktime(time.strptime(str(newstartdate_var), pattern)))
        epochEnd = int(time.mktime(time.strptime(str(newenddate_var), pattern)))
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
