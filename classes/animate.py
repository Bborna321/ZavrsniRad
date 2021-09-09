import numpy as np
import mplfinance as mpf
from classes.components.datamanager import *
from matplotlib.widgets import Slider
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")


def animate(_, anio, pause, options, tactics, moneyManager):
    if not pause:
        leftValue = max(0, tactics.ival - 50)
        rightValue = tactics.ival
        data = tactics.data

        if tactics.ival >= len(data):
            Log(tactics.options.mylist, ["Fetching more data"])
            CreateMoreData()
            noMoreData = tactics.LoadMoreData()
            if noMoreData:
                anio.event_source.stop()
                Log(tactics.options.mylist, ["No more data"])
            return

        ap, ax1, ax2 = tactics.GetAnimationData(leftValue, rightValue, options.toAnimate)

        plotdata = data.iloc[leftValue:rightValue]

        ax1.clear()
        ax2.clear()

        moneyManager.Trader(plotdata['open'][-1], plotdata['close'][-1],
                             plotdata['high'][-1], plotdata['low'][-1],
                             plotdata['date'][-1], options)

        if options.toTrade[1] == 1:
            tactics.MACDTrader(options, moneyManager)
        if options.toTrade[2] == 1:
            tactics.FIBOTrader(options, moneyManager, plotdata, leftValue, rightValue)
        if options.toTrade[3] == 1:
            tactics.BollRSITrader(options, moneyManager, leftValue, rightValue)



        tactics.ival = tactics.ival + 1

        enterDates, exitDates = CatchEntersExits(plotdata, moneyManager)

        apEnter = mpf.make_addplot(enterDates, type="scatter", ax=ax1, markersize=200, color='blue', alpha=0.6)
        apExit = mpf.make_addplot(exitDates, type="scatter", ax=ax1, markersize=150, color='orange', alpha=0.6)

        ap.append(apEnter)
        ap.append(apExit)

        mpf.plot(plotdata, addplot=ap, type='candle', ax=ax1)



def CatchEntersExits(plotdata, moneyManager):
    enterTradeCatcher = []
    exitTradeCatcher = []
    for i in range(plotdata['date'].values.shape[0]):
        if plotdata['date'][i] in moneyManager.tradingStarts:
            enterTradeCatcher.append(plotdata['open'][i])
        else:
            enterTradeCatcher.append(np.nan)
        if plotdata['date'][i] in moneyManager.tradingStops:
            exitTradeCatcher.append(plotdata['open'][i])
        else:
            exitTradeCatcher.append(np.nan)
    return enterTradeCatcher, exitTradeCatcher
