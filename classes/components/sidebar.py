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


class Options:
    def __init__(self, tabControl, controller, money_manager):
        self.toAnimate = [0, 0, 0, 0, 0]
        self.startdate = "1531216800"
        self.enddate = "1551648800"
        self.jsonObject = GetJsonData()
        self.oldCoin = self.jsonObject['coin']

        parent = Frame(tabControl)
        botSettings = Frame(tabControl)

        tabControl.add(parent, text='Graph Settings')
        tabControl.add(botSettings, text='Bot Settings')

        self.__GraphSettings(parent)
        self.__BotSettings(botSettings, money_manager)

    def __GraphSettings(self, parent):
        coinlabel = ttk.Label(parent, text="Change coin: ", font=normal_font)
        coinlabel.pack()

        newcoin_var = tk.StringVar()
        coin = Entry(parent, textvariable=newcoin_var)
        coin.insert(0, self.jsonObject['coin'])
        coin.pack()
        coin.bind("<Button-1>", lambda _: self.newPlaceholder(coin, self.jsonObject, 'coin', newcoin_var.get()))
        coin.bind("<FocusOut> ", lambda _: self.ChangePlaceholder(coin, newcoin_var.get(), self.jsonObject['coin']))

        currencylabel = ttk.Label(parent, text="Change currency: ", font=normal_font)
        currencylabel.pack()

        newcurrency_var = tk.StringVar()
        currency = Entry(parent, textvariable=newcurrency_var)
        currency.insert(0, self.jsonObject['fiat'])
        currency.pack()
        currency.bind("<Button-1>",
                      lambda _: self.newPlaceholder(currency, self.jsonObject, 'fiat', newcurrency_var.get()))
        currency.bind("<FocusOut> ",
                      lambda _: self.ChangePlaceholder(currency, newcurrency_var.get(), self.jsonObject['fiat']))
        currency.bind("<Leave> ", lambda _: self.ChangePlaceholder(coin, newcoin_var.get(), self.jsonObject['coin']))

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

        startCal.bind("<<DateEntrySelected>>", lambda _: self.DateToEpoch(startCal, endCal))
        endCal.bind("<<DateEntrySelected>>", lambda _: self.DateToEpoch(startCal, endCal))

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

        sub_btn = tk.Button(parent, text='Submit',
                            command=lambda: self.Submit([var1.get(), var2.get(), var3.get(), var4.get(), 0],
                                                        newcoin_var, newcurrency_var))
        sub_btn.pack()

    def __BotSettings(self, botSettings, money_manager):
        jsonObjectMoney = GetJsonDataMoney()

        current_money_str_var = tk.StringVar()
        curr_mon = Entry(botSettings, text=current_money_str_var)
        curr_mon.insert(0, jsonObjectMoney['current_money'])
        curr_mon.pack()
        curr_mon.bind("<Button-1>",
                      lambda _: self.newPlaceholder(curr_mon, jsonObjectMoney, "current_money",
                                                    current_money_str_var.get()))
        curr_mon.bind("<FocusOut> ", lambda _: self.ChangePlaceholder(curr_mon, current_money_str_var.get(),
                                                                      jsonObjectMoney['current_money']))

        start_tradeing_btn = tk.Button(botSettings, text='Enter Trade', command=lambda: self.enter_trade(money_manager))
        start_tradeing_btn.pack()

        stop_tradeing_btn = tk.Button(botSettings, text='Exit Trade', command=lambda: self.exit_trade(money_manager))
        stop_tradeing_btn.pack()

    def enter_trade(self, money_manager):
        money_manager.in_trading = True
        print("u enteru sam")

    def exit_trade(self, money_manager):
        money_manager.in_trading = False
        print("u exitu sam")

    def Submit(self, variables, newcoin_var, newcurrency_var):
        self.toAnimate = variables
        print(self.toAnimate)
        CreateJson(newcoin_var.get(), newcurrency_var.get(), self.oldCoin, self.startdate,
                   self.enddate)

    def DateToEpoch(self, startCal, endCal):
        newstartdate_var = startCal.get_date()
        newenddate_var = endCal.get_date()
        pattern = '%Y-%m-%d'
        epochStart = int(time.mktime(time.strptime(str(newstartdate_var), pattern)))
        epochEnd = int(time.mktime(time.strptime(str(newenddate_var), pattern)))
        self.startdate = epochStart
        self.enddate = epochEnd

    def newPlaceholder(self, entry, jsonobject, ob, value):
        entry.delete(0, 'end')
        print(value)
        if not value == "":
            jsonobject[ob] = value

    def ChangePlaceholder(self, entry, value, jsonObject):
        print(value)
        if value == "":
            entry.insert(0, jsonObject)

    def ChangePlaceholderMoney(self, entry, value, jsonObject):
        try:
            entry.insert(0, jsonObject)
        except Exception:
            print("ne meže, sori", Exception)


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