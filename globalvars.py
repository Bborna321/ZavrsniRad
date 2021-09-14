from matplotlib import style
from matplotlib.figure import Figure

largeFont = ('Verdana', 12)
normalFont = ('Verdana', 10)
smallFont = ('Verdana', 8)
style.use('ggplot')

darkColor = "#892020"
lightColor = "#208989"
lightColor_prev = "#7fff00"
amethyst = "#9966cc"
aurelion = "#fdee00"
atomic_tangerine = "#ff9966"

f = Figure(figsize=(21, 9), dpi=90)
a = f.add_subplot(111)

interval_of_animation = 10

brojac = 0

chartLoad = True

market = "LTC-EUR"
granularity = 86400

macdOnOff = "off"
BollingerOnOff = "on"

currentMoneyStart = 100
currentMoney = 100
sellAtHigh = 120
sellAtLow = 84
