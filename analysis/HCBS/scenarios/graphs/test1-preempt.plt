set terminal png size 800,800
set yrange [0:5000]

set title "Preemptions"
set xlabel "number of non RT containers"
set ylabel "Preemptions"
set grid
plot "data1preeempt.dat" u (column(0)):2:xtic(1) w l title "overhead (T = 100 ms)", "data1preeempt.dat" u (column(0)):3:xtic(1) w l title "overhead (T = 10 ms)", "data1preeempt.dat" u (column(0)):4:xtic(1) w l title "overhead (T = 1 ms)"