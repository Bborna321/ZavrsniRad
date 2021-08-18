import matplotlib;
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
        # plotdata = data.iloc[:]

        ax1.clear()
        # mpf.plot(plotdata, ax=ax1, addplot=ap,type="candle")

        mpf.plot(plotdata, type='candle', addplot=ap, ax=ax1)

        if options.toAnimate[0] == 1:
            tactics.faj(options, money_manager)

        tactics.ival = tactics.ival + 1

        money_manager.trader(plotdata['close'][-2], plotdata['close'][-1],
                             plotdata['high'][-1], plotdata['low'][-1])
