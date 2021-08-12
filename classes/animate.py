import matplotlib;

matplotlib.use("TkAgg")
import mplfinance as mpf
from classes.components.datamanager import GetData
import pandas as pd
from global_vars import *

def animate(ival, anio,ax1):
    data = GetData()
    if (20+ival) > len(data):
        print('no more data to plot')
        anio.event_source.interval *= 3
        if anio.event_source.interval > 12000:
            exit()
        return


    # To plot whole data use len(data) instead of (20+ival)
    plotdata = data.iloc[0:(20+ival)]
    emaData = plotdata['close']
    dates_plot = list(plotdata['date'].values)
    dfEma = pd.DataFrame(emaData)
    mean20 = dfEma.ewm(span=20).mean()
    std20 = dfEma.ewm(span=20).std()
    ax1.clear()
    dates_plot.sort()
    ax1.plot_date(dates_plot, mean20 + 2 * std20, amethyst, label="upper")
    ax1.plot_date(dates_plot, mean20 - 2 * std20, amethyst, label="lower")
    mpf.plot(plotdata,ax=ax1,type='candle')

