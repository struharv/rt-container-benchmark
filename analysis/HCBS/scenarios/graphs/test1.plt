set terminal png size 800,800
set yrange [0:40]

set title "Overhead"
set xlabel "Number of non RT containers"
set ylabel "Overhead [CPU time %]"
set grid
plot "data1.dat" u (column(0)):2:xtic(1) w l title "Overhead (T = 100 ms, Q = 30 ms)", "data1.dat" u (column(0)):3:xtic(1) w l title "Overhead (T = 10 ms, Q = 3 ms)", "data1.dat" u (column(0)):4:xtic(1) w l title "Overhead (T = 1 ms, T=300 us)"
