import matplotlib;

from classes.macd import Macd

matplotlib.use("TkAgg")
import mplfinance as mpf
from classes.BollingerBands import BollingerBands
from classes.FibonacciRetracement import FibonacciRetracement
from classes.RSI import RSI

ival = 20


def animate(_, anio, ax1, pause, toAnimate, tactics):
    global ival
    if not pause:
        data, ap, ax1 = tactics.GetAnimationData(ival, toAnimate)

        if ival > len(data):
            print('no more data to plot')
            anio.event_source.interval *= 3
            if anio.event_source.interval > 12000:
                exit()
            return

        # To plot whole data use ":" instead of "(20+ival)"
        plotdata = data.iloc[0:ival]
        #plotdata = data.iloc[:]

        ax1.clear()
        #mpf.plot(plotdata, ax=ax1, addplot=ap,type="candle")

        mpf.plot(plotdata, type='candle', addplot=ap, ax=ax1)

        ival = ival + 1
