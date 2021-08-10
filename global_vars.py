from matplotlib import style
from matplotlib.figure import Figure


large_font=('Verdana',12)
normal_font=('Verdana',10)
small_font=('Verdana',8)
style.use('ggplot')

darkColor = "#892020"
lightColor = "#208989"
lightColor_prev = "#7fff00"

f = Figure(figsize=(21,9), dpi=90)
#f = Figure()
a = f.add_subplot(111)

exchange = "BTC-e"
DatCounter = 9000
programName = "coinbase"

resampleSize = "15Min"
dataPace="tick"
candleWidth = 0.008
paneCount=1

topIndicator="none"
botIndicator="none"
midIndicator="none"
EMAs=[]
SMAs=[]
chartLoad=True

market = "LTC-EUR"
granularity = 86400

macdOnOff = "off"