#set yrange [0:400000000]
set terminal png size 800,800
set xlabel "instance"
set ylabel "period"


plot 'points_period.dat' w p ls 1 
