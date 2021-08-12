from matplotlib import style
from matplotlib.figure import Figure


large_font=('Verdana',12)
normal_font=('Verdana',10)
small_font=('Verdana',8)
style.use('ggplot')

darkColor = "#892020"
lightColor = "#208989"
lightColor_prev = "#7fff00"
amethyst = "#9966cc"
aurelion = "#fdee00"
atomic_tangerine = "#ff9966"

f = Figure(figsize=(21,9), dpi=90)
#f = Figure()
a = f.add_subplot(111)

interval_of_animation=10

brojac=0

chartLoad=True

market = "LTC-EUR"
granularity = 86400

macdOnOff = "off"
BollingerOnOff ="on"