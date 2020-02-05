# set yrange [0:]
set terminal png size 800,800
set xlabel "instance"
set ylabel "runtime"


plot 'points_runtime.dat' w p ls 1, 400000000
