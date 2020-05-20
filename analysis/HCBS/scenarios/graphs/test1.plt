set terminal png size 800,800
set yrange [0:40]

set title "stability of RT containers"
set xlabel "number of non RT containers"
set ylabel "CPU time %"
set grid
plot "data1.dat" u (column(0)):2:xtic(1) w l title "overhead (P = 100 ms)", "data1.dat" u (column(0)):3:xtic(1) w l title "overhead (P = 10 ms)", "data1.dat" u (column(0)):4:xtic(1) w l title "overhead (P = 1 ms)"