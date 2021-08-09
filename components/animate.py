from global_vars import *
import finplot as fplt
import matplotlib.ticker as mticker
import historical_data as hsd
import global_vars as gv
from mplfinance.original_flavor import candlestick_ohlc


import pandas as pd
def animate_real_deal(_):
    global refreshRate
    global DatCounter
    global firstLoadOfGraph
    if chartLoad:
        if paneCount == 1:
            if dataPace=="tick":
                try:

                    #a = plt.subplot2grid((6,2),(0,0),rowspan=5,colspan=4)
                    #print(a)
                    #a2 = plt.subplot2grid((6,2),(5,0),rowspan=1,colspan=4,sharex=a)

                    data = hsd.cbpGetHistoricRates(gv.market, granularity=gv.granularity)
                    #data_ohlc = hsd.

                    a.clear()

                    a.set_xlabel('Date')
                    a.set_ylabel('Price')


                    """jedan koristi ohlc a jedan ohcl!!! ....."""


                    candlestick_ohlc(a,data.values(),width=2,colordown=darkColor,colorup=lightColor)

                    #df = pd.DataFrame(data.values(), columns='time open high low close'.split())
                    #fplt.candlestick_ochl(df[['time', 'open', 'close', 'high', 'low']],a)

                    #a.plot_date(dates_plot, values_plot_close, darkColor, label='close')
                    #a.plot_date(dates_plot,values_plot_open,lightColor,label='open')
                    a.xaxis.set_major_locator(mticker.MaxNLocator(11))
                    a.grid(True)
                    #date_format = mdates.DateFormatter('%Y-%m-%d')
                    #print(date_format)
                    #a.xaxis.set_major_formatter(date_format)

                    #a.legend(bbox_to_anchor=(0,1.02,1,.102),loc=4,ncol=2,borderaxespad=0)
                    last_price=''
                    for vals in data.values().__reversed__():
                        last_price=str(vals[-1])

                    title = gv.market.split('-')[0] +' historical data\nLast price: '+last_price+' '+ gv.market.split('-')[1]
                    a.set_title(title)
                except Exception as e:
                    print("Failed because of:",e)
            fplt.show()