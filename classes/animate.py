import matplotlib;

from classes.macd import Macd

matplotlib.use("TkAgg")
import mplfinance as mpf
from classes.BollingerBands import BollingerBands
from classes.FibonacciRetracement import FibonacciRetracement
from classes.RSI import RSI

ival = 0


def animate(_, anio, ax1, pause):
    global ival
    if not pause:
        #fibo = FibonacciRetracement((20 + ival), ax1)
        #data, ap, ax1 = fibo.GetAnimationData()
        #rsi = RSI((20 + ival), ax1)
        #data, ap, ax1 = rsi.GetAnimationData()
        #boll = BollingerBands((20 + ival), ax1)
        #data, ap, ax1 = boll.GetAnimationData()
        macd = Macd((20 + ival), ax1)
        data, ap, ax1 = macd.GetAnimationData()


        if (20 + ival) > len(data):
            print('no more data to plot')
            anio.event_source.interval *= 3
            if anio.event_source.interval > 12000:
                exit()
            return


        # To plot whole data use : instead of (20+ival)
        plotdata = data.iloc[0:(20 + ival)]
        #plotdata = data.iloc[:]

        ax1.clear()
        mpf.plot(plotdata, ax=ax1, addplot=ap, type='candle')
        ival = ival + 1
