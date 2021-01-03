set terminal png size 800,800
set yrange [0:40]

set title "stability of RT containers"
set xlabel "number of non RT containers"
set ylabel "CPU time %"
set grid
plot "data2.dat" u (column(0)):2:xtic(1) w l title "overhead (T = 100 ms)", "data2.dat" u (column(0)):3:xtic(1) w l title "overhead (T = 10 ms)"