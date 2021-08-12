import pandas.plotting

from global_vars import *
import finplot as fplt
import matplotlib.ticker as mticker
import historical_data as hsd
import global_vars as gv
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.pyplot as plt
import numpy as np
import classes.BollingerBands as BollingerBands

import pandas as pd


def animate_real_deal(_):
    global refreshRate
    global DatCounter
    global firstLoadOfGraph

    def computeMCAD(x, location="bottom"):
        values = {"key": 1, "prices": x}

        url = 12;

    if gv.chartLoad:
        gv.chartLoad = False
        try:

            # a = plt.subplot2grid((6,2),(0,0),rowspan=5,colspan=4)
            # print(a)
            # a2 = plt.subplot2grid((6,2),(5,0),rowspan=1,colspan=4,sharex=a)

            data = hsd.cbpGetHistoricRates(gv.market, granularity=gv.granularity)
            # data_ohlc = hsd.

            a.clear()

            a.set_xlabel('Date')
            a.set_ylabel('Price')

            """jedan koristi ohlc a jedan ohcl!!! ....."""

            print("tu sam i greška je ispod")

            candlestick_ohlc(a, data.values(), width=0.8, colordown=darkColor, colorup=lightColor)

            # df = pd.DataFrame(data.values(), columns='time open high low close'.split())
            # fplt.candlestick_ochl(df[['time', 'open', 'close', 'high', 'low']],a)

            values_plot_close = []
            dates_plot = []
            for date, val in data.items():
                values_plot_close.append(val[4])
                dates_plot.append(val[0])

            # a.plot_date(dates_plot, values_plot_close, darkColor, label='close')
            # a.plot_date(dates_plot,values_plot_open,lightColor,label='open')
            a.xaxis.set_major_locator(mticker.MaxNLocator(11))
            # a.grid(True)
            # date_format = mdates.DateFormatter('%Y-%m-%d')
            # print(date_format)
            # a.xaxis.set_major_formatter(date_format)

            # print(gv.macdOnOff)
            emaData = {"Price": values_plot_close}
            dfEma = pd.DataFrame(emaData)
            if gv.macdOnOff == "on":

                mean12 = dfEma.ewm(span=12).mean()
                mean26 = dfEma.ewm(span=26).mean()
                a.plot_date(dates_plot, mean12, amethyst, label='ema10')
                a.plot_date(dates_plot, mean26, atomic_tangerine, label='ema26')

                macd = mean12 - mean26
                signal_line = macd.ewm(span=9).mean()

                histogram = macd - signal_line

                a.plot_date(dates_plot, histogram, "black", label="histogram")
                a.plot_date(dates_plot, histogram * 0, aurelion, label="kernell")


            elif gv.BollingerOnOff == "on":
                mean20 = dfEma.ewm(span=20).mean()
                a.plot_date(dates_plot, mean20, "red", label="ema20")

                std20 = dfEma.ewm(span=20).std()

                a.plot_date(dates_plot, mean20 + 2 * std20, amethyst, label="upper")
                a.plot_date(dates_plot, mean20 - 2 * std20, amethyst, label="lower")

            a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=4, ncol=2, borderaxespad=0)

            last_price = ''
            for vals in data.values().__reversed__():
                last_price = str(vals[-1])

            title = gv.market.split('-')[0] + ' historical data\nLast price: ' + str(
                round(float(last_price), 2)) + ' ' + gv.market.split('-')[1]
            a.set_title(title)
        except Exception as e:
            print("Failed because of:", e)
        gv.interval_of_animation = 600000
        # fplt.show()
