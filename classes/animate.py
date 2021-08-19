import numpy as np
import matplotlib
from classes.components.datamanager import *

matplotlib.use("TkAgg")
import mplfinance as mpf


def animate(_, anio, ax1, pause, options, tactics, money_manager):
    # ival = tactics.ival + 20
    if not pause:
        leftValue = max(0, tactics.ival - 50)
        rightValue = tactics.ival
        data = tactics.data

        if tactics.ival >= len(data):
            CreateMoreData()
            tactics.LoadMoreData()
            if anio.event_source.interval > 12000:
                exit()
            return

        ap, ax1 = tactics.GetAnimationData(leftValue, rightValue, options.toAnimate)
        # To plot whole data use ":" instead of "(20+tactics.ival)"
        plotdata = data.iloc[leftValue:rightValue]

        ax1.clear()
        if options.toAnimate[0] == 1:
            tactics.faj(options, money_manager)

        tactics.ival = tactics.ival + 1

        money_manager.trader(plotdata['close'][-2], plotdata['close'][-1],
                             plotdata['high'][-1], plotdata['low'][-1],
                             plotdata['date'][-1])
        enter_dates, exit_dates = catch_enters_exits(plotdata, money_manager)

        ap_enter = mpf.make_addplot(enter_dates,type="scatter",ax=ax1)
        ap_exit = mpf.make_addplot(exit_dates, type="scatter",ax=ax1)

        ap.append(ap_enter)
        ap.append(ap_exit)

        mpf.plot(plotdata, addplot=ap, type='candle', ax=ax1)

def catch_enters_exits(plotdata, money_manager):
    enter_trade_catcher = []
    exit_trade_catcher = []
    for date in plotdata['date']:
        if date in money_manager.trading_starts:
            enter_trade_catcher.append(date)
        else:
            enter_trade_catcher.append(np.nan)
        if date in money_manager.trading_stops:
            exit_trade_catcher.append((date))
        else:
            exit_trade_catcher.append(np.nan)
    return enter_trade_catcher,exit_trade_catcher
