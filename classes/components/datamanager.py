import pandas as pd
import matplotlib.dates as mdates
import historical_data as hsd
import json
from tkinter import *


def CreateMoreData():
    jsonObject = GetJsonData('data.json')
    iso8601end = jsonObject['iso8601end']
    iso8601start = str(int(iso8601end))
    iso8601end = str(int(iso8601start) + 86400*180)
    CreateJson(iso8601start=iso8601start, iso8601end=iso8601end)


def GetData():
    data = pd.read_csv('file.csv')
    data = data.set_index(pd.DatetimeIndex(data["date"].values))
    data["date"] = pd.to_datetime(data['date'])
    data["date"] = data["date"].apply(mdates.date2num)
    return data


def CreateJson(coin="LTC", fiat="EUR", oldcoin="LTC", iso8601start="1531216800", iso8601end="1551610800"):
    dic = {"coin": coin, "fiat": fiat, "oldcoin": oldcoin, "iso8601start": iso8601start, "iso8601end": iso8601end}
    with open("data.json", "w+") as jsonFile:
        json.dump(dic, jsonFile)

    hsd.cbpGetHistoricRates()


def CreateJsonMoney(current_money=100.0, sell_high=1.2, sell_low=0.84):
    if sell_high < sell_low:
        temp = sell_high
        sell_high = sell_low
        sell_low = temp

    if sell_high < 1:
        sell_high = 2 - sell_high
    if sell_low > 1:
        sell_low = 2 - sell_low

    sell_high_val = current_money * sell_high
    sell_low_val = current_money * sell_low
    dic = {"current_money": str(current_money), "sell_high": str(sell_high), "sell_low": str(sell_low),
           "sell_high_val": str(sell_high_val), "sell_low_val": str(sell_low_val)}
    with open("data_money.json", "w+") as jsonFile:
        json.dump(dic, jsonFile)


def GetJsonData(fileName):
    with open(fileName) as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    return jsonObject


def ChangeCoing(newcoin_var):
    with open("data.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data["oldcoin"] = data["coin"]
    data["coin"] = newcoin_var.get()

    with open("data.json", "w") as jsonFile:
        json.dump(data, jsonFile)

    hsd.cbpGetHistoricRates()

    data = GetData()
    return data


def Log(mylist, text, color="black"):
    for t in text:
        mylist.insert(END, t)
        mylist.itemconfig(mylist.size() - 1, foreground=color)

