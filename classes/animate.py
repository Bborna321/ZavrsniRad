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


def animate(_, anio, ax1, pause, options, tactics, money_manager):
    #ival = tactics.ival + 20
    if not pause:
        data, ap, ax1 = tactics.GetAnimationData(tactics.ival, options.toAnimate)

        if tactics.ival > len(data):
            #print('no more data to plot')
            anio.event_source.interval *= 3
            if anio.event_source.interval > 12000:
                exit()
            return

        # To plot whole data use ":" instead of "(20+tactics.ival)"
        plotdata = data.iloc[max(0,tactics.ival-50):tactics.ival]
        #plotdata = data.iloc[:]

        ax1.clear()
        #mpf.plot(plotdata, ax=ax1, addplot=ap,type="candle")

        mpf.plot(plotdata, type='candle', addplot=ap, ax=ax1)

        if options.toAnimate[0] == 1:
            tactics.faj(options,money_manager)

        tactics.ival = tactics.ival + 1

        money_manager.trader(plotdata['close'][-2], plotdata['close'][-1],
                                   plotdata['high'][-1], plotdata['low'][-1])


