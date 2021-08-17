import pandas as pd
import matplotlib.dates as mdates
import historical_data as hsd
import json
import csv


def GetData():
    data = pd.read_csv('file.csv')
    data = data.set_index(pd.DatetimeIndex(data["date"].values))
    data["date"] = pd.to_datetime(data['date'])
    data["date"] = data["date"].apply(mdates.date2num)
    return data


def CreateJson(coin="BTC", fiat="EUR", oldcoin="BTC", iso8601start="153121800", iso8601end="1551648800"):
    dic = {"coin": coin, "fiat": fiat, "oldcoin": oldcoin, "iso8601start": iso8601start, "iso8601end": iso8601end}
    with open("data.json", "w+") as jsonFile:
        json.dump(dic, jsonFile)
    hsd.cbpGetHistoricRates()


def CreateJsonMoney(current_money=100.0,sell_high=1.2,sell_low=0.84):

    if sell_high < sell_low:
        temp = sell_high
        sell_high = sell_low
        sell_low = temp

    if sell_high<1:
        sell_high = 2-sell_high
    if sell_low>1:
        sell_low = 2-sell_low

    sell_high_val = current_money*sell_high
    sell_low_val = current_money * sell_low
    dic = {"current_money":str(current_money),"sell_high":str(sell_high),"sell_low":str(sell_low),
           "sell_high_val":str(sell_high_val),"sell_low_val":str(sell_low_val)}
    with open("data_money.json", "w+") as jsonFile:
        json.dump(dic, jsonFile)


def GetJsonData():
    with open("data.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    return jsonObject

def GetJsonDataMoney():
    with open("data_money.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    return jsonObject

def GetJsonDataMoneySellLowSellHigh():
    with open("data_money.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        print("SEll low:", jsonObject['sell_low'])
        jsonFile.close()
    return float(jsonObject['sell_low']),float(jsonObject['sell_high'])

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



