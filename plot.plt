# set the terminal, i.e., the figure format (eps) and font (Helvetica, 20pt)
set term postscript eps enhanced "Helvetica" 20 

# reset all options to default, just for precaution
reset

# set the figure size
set size 0.7,0.7

# set the figure name
set output "loss.eps"

# set the x axis
set xrange [0:100]
set xlabel "Buffer size (packets)"
set xtics 0,20,100
set mxtics 2

# set the y axis
set logscale y
set yrange [1e-3:1]
set ylabel "Packet loss ratio"
set format y "1e{%L}"
set mytics 10

# set the legend (boxed, on the bottom)
set key box bottom height 0.5

# set the grid (grid lines start from tics on both x and y axis)
set grid xtics ytics

# set the mu parameter
mu = 1000.0

# l(K,lambda) is the theoretical loss ratio at steady state
l(K,lambda) = lambda==mu ? 1.0/(K+1) : ((1.0-lambda/mu)*(lambda/mu)**K)/(1.0-(lambda/mu)**(K+1))

# plot the data from the log file along with the theoretical curve
plot "loss_500.log" u 4:5 t "{/Symbol l} = 500" w p pt 1 ps 2 lc rgb "#AAAAAA", \
     l(x,500) t "" w l lt 1 lw 1 lc rgb "#000000", \
     "loss_700.log" u 4:5 t "{/Symbol l} = 700" w p pt 2 ps 2 lc rgb "#AAAAAA", \
     l(x,700) t "" w l lt 1 lw 1 lc rgb "#000000", \
     "loss_900.log" u 4:5 t "{/Symbol l} = 900" w p pt 5 ps 2 lc rgb "#AAAAAA", \
     l(x,900) t "" w l lt 1 lw 1 lc rgb "#000000", \
     "loss_1000.log" u 4:5 t "{/Symbol l} = 1000" w p pt 7 ps 2 lc rgb "#AAAAAA", \
     l(x,1000) t "" w l lt 1 lw 1 lc rgb "#000000", \
     "loss_1100.log" u 4:5 t "{/Symbol l} = 1100" w p pt 9 ps 2 lc rgb "#AAAAAA", \
     l(x,1100) t "" w l lt 1 lw 1 lc rgb "#000000", \
     "loss_1300.log" u 4:5 t "{/Symbol l} = 1300" w p pt 11 ps 2 lc rgb "#AAAAAA", \
     l(x,1300) t "" w l lt 1 lw 1 lc rgb "#000000"

