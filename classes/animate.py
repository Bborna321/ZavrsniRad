import numpy as np
import mplfinance as mpf
from classes.components.datamanager import *
from matplotlib.widgets import Slider
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")


def animate(_, anio, ax_slider, pause, options, tactics, money_manager):
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

        ap, ax1 = tactics.GetAnimationData(leftValue, rightValue, options.toAnimate)

        plotdata = data.iloc[leftValue:rightValue]

        ax1.clear()
        if options.toAnimate[0] == 1:
            tactics.MACDTrader(options, money_manager)

        tactics.ival = tactics.ival + 1

        money_manager.trader(plotdata['close'][-2], plotdata['close'][-1],
                             plotdata['high'][-1], plotdata['low'][-1],
                             plotdata['date'][-1])
        enter_dates, exit_dates = catch_enters_exits(plotdata, money_manager)

        ap_enter = mpf.make_addplot(enter_dates, type="scatter", ax=ax1, markersize=100, color='blue', alpha=0.6)
        ap_exit = mpf.make_addplot(exit_dates, type="scatter", ax=ax1, markersize=100, color='orange', alpha=0.6)

        ap.append(ap_enter)
        ap.append(ap_exit)

        mpf.plot(plotdata, addplot=ap, type='candle', ax=ax1)



def catch_enters_exits(plotdata, money_manager):
    enter_trade_catcher = []
    exit_trade_catcher = []
    for i in range(plotdata['date'].values.shape[0]):
        if plotdata['date'][i] in money_manager.trading_starts:
            enter_trade_catcher.append(plotdata['close'][i])
        else:
            enter_trade_catcher.append(np.nan)
        if plotdata['date'][i] in money_manager.trading_stops:
            exit_trade_catcher.append(plotdata['close'][i])
        else:
            exit_trade_catcher.append(np.nan)
    return enter_trade_catcher, exit_trade_catcher
