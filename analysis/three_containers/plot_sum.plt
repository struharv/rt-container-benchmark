set boxwidth 0.5
set style fill solid
set yrange [0:]
set terminal png size 800,800
plot "points_sum.dat" using 1:3:xtic(2) with boxes, "tmp.dat"
