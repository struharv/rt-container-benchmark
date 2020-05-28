set terminal png size 800,800
set yrange [0:40]

set title "Overhead"
set xlabel "number of non RT containers"
set ylabel "CPU time %"
set grid
plot "data1.dat" u (column(0)):2:xtic(1) w l title "overhead (T = 100 ms)", "data1.dat" u (column(0)):3:xtic(1) w l title "overhead (T = 10 ms)", "data1.dat" u (column(0)):4:xtic(1) w l title "overhead (T = 1 ms)"