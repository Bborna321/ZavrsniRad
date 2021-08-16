import matplotlib;

import global_vars as gv
from classes import money_manager as money_manager_imp
import classes.money_manager
from classes.macd import Macd

matplotlib.use("TkAgg")
import mplfinance as mpf
from classes.BollingerBands import BollingerBands
from classes.FibonacciRetracement import FibonacciRetracement
from classes.RSI import RSI
import classes.money_manager

ival = 20


def animate(_, anio, ax1, pause, toAnimate, tactics, money_manager):
    global ival
    if not pause:
        data, ap, ax1 = tactics.GetAnimationData(ival, toAnimate)

        if ival > len(data):
            #print('no more data to plot')
            anio.event_source.interval *= 3
            if anio.event_source.interval > 12000:
                exit()
            return

        # To plot whole data use ":" instead of "(20+ival)"
        plotdata = data.iloc[max(0,ival-50):ival]
        #plotdata = data.iloc[:]

        ax1.clear()
        #mpf.plot(plotdata, ax=ax1, addplot=ap,type="candle")
        mpf.plot(plotdata, type='candle', addplot=ap, ax=ax1)

        ival = ival + 1


        money_manager.trader(plotdata['close'][-2], plotdata['close'][-1],
                                   plotdata['high'][-1], plotdata['low'][-1])

        print("current money",money_manager.current_money,"trading status:",money_manager.in_trading)
