import pandas as pd
import matplotlib.dates as mdates
import historicaldata as hsd
import json
from tkinter import *
import os



def CreateMoreData():
    jsonObject = GetJsonData('data.json')
    iso8601end = jsonObject['iso8601end']
    iso8601start = str(int(iso8601end))
    iso8601end = str(int(iso8601start) + 86400 * 180)
    CreateJson(jsonObject['coin'], jsonObject['fiat'], jsonObject['oldcoin'],
               iso8601start=iso8601start, iso8601end=iso8601end)


def GetData():
    data = pd.read_csv('file.csv')
    data = data.set_index(pd.DatetimeIndex(data["date"].values, dayfirst=True))
    data["date"] = pd.to_datetime(data['date'], dayfirst=True)
    data["date"] = data["date"].apply(mdates.date2num)
    return data


def CreateJson(coin="LTC", fiat="EUR", oldcoin="LTC", iso8601start="1531216800", iso8601end="1551610800"):
    try:
        jsonObject = GetJsonData('data.json')
        dic = {"coin": coin, "fiat": fiat, "oldcoin": oldcoin, "iso8601start": iso8601start, "iso8601end": iso8601end,
               "start": jsonObject['start'], "end": jsonObject['end']}
        with open("data.json", "w+") as jsonFile:
            json.dump(dic, jsonFile)
    except:
        dic = {"coin": coin, "fiat": fiat, "oldcoin": oldcoin, "iso8601start": iso8601start, "iso8601end": iso8601end,
               "start": iso8601start, "end": iso8601end}
        with open("data.json", "w+") as jsonFile:
            json.dump(dic, jsonFile)
    hsd.cbpGetHistoricRates()


def CreateJsonMoney(currentMoney=100.0, sellHigh=1.2, sellLow=0.84):
    if sellHigh < sellLow:
        temp = sellHigh
        sellHigh = sellLow
        sellLow = temp

    if sellHigh < 1:
        sellHigh = 2 - sellHigh
    if sellLow > 1:
        sellLow = 2 - sellLow

    sellHighVal = currentMoney * sellHigh
    sellLowVal = currentMoney * sellLow
    dic = {"current_money": str(currentMoney), "sell_high": str(sellHigh), "sell_low": str(sellLow),
           "sell_high_val": str(sellHighVal), "sell_low_val": str(sellLowVal)}
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

def DeleteFile(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)
