from global_vars import *
import finplot as fplt
import matplotlib.ticker as mticker
import historical_data as hsd
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.dates import DayLocator, date2num, DateFormatter
import json
import pandas as pd


def animate_real_deal(_):
    with open("data.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    market = jsonObject["coin"] + "-" + jsonObject["fiat"]
    global data
    global refreshRate
    global DatCounter
    global firstLoadOfGraph
    if chartLoad:
        if paneCount == 1:
            if dataPace == "tick":
                try:

                    data = hsd.cbpGetHistoricRates()
                    # a = plt.subplot2grid((6,2),(0,0),rowspan=5,colspan=4)
                    # print(a)
                    # a2 = plt.subplot2grid((6,2),(5,0),rowspan=1,colspan=4,sharex=a)
                    # data_ohlc = hsd.

                    a.clear()

                    a.set_xlabel('Date')
                    a.set_ylabel('Price')

                    """jedan koristi ohlc a jedan ohcl!!! ....."""
                    candlestick_ohlc(a, data.values(), width=1, colordown=darkColor, colorup=lightColor)

                    #df = pd.DataFrame(data.values(), columns='time open high low close'.split())
                    #fplt.candlestick_ochl(df[['time', 'open', 'close', 'high', 'low']],a)

                    # a.plot_date(dates_plot, values_plot_close, darkColor, label='close')
                    # a.plot_date(dates_plot,values_plot_open,lightColor,label='open')
                    a.xaxis.set_major_locator(DayLocator())
                    a.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
                    a.xaxis.set_major_locator(mticker.MaxNLocator(11))
                    a.grid(True)
                    # date_format = mdates.DateFormatter('%Y-%m-%d')
                    # print(date_format)
                    # a.xaxis.set_major_formatter(date_format)

                    # a.legend(bbox_to_anchor=(0,1.02,1,.102),loc=4,ncol=2,borderaxespad=0)
                    last_price = ''
                    for vals in data.values().__reversed__():
                        last_price = str(vals[-1])

                    title = market.split('-')[0] + ' historical data\nLast price: ' + last_price + ' ' + \
                            market.split('-')[1]
                    a.set_title(title)
                except Exception as e:
                    print("Failed because of:", e)
                    with open("data.json", "r") as jsonFile:
                        data = json.load(jsonFile)

                    data["coin"] = data["oldcoin"]

                    with open("data.json", "w") as jsonFile:
                        json.dump(data, jsonFile)
            fplt.show()
