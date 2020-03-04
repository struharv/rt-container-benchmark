set yrange [0:700000000]
set terminal png size 800,800
set xlabel "instance"
set ylabel "runtime"


plot 'points_runtime.dat' w p ls 1, 'points_runtime1.dat' w p ls 2,  500000000, 400000000, 100000000 
