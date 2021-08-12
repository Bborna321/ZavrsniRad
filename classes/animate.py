import matplotlib;

matplotlib.use("TkAgg")
import mplfinance as mpf
from classes.components.datamanager import GetData

datatotake = 5
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
    ax1.clear()
    mpf.plot(plotdata,ax=ax1,type='candle')


