set title "Latency plot"
set terminal png
set xlabel "Latency (us)"
set logscale y
set xrange [0:600]
set yrange [0.8:*]
set ylabel "Number of latency samples"
set output "plot.png"
plot "test2/histogram" using 1:2 with line title "1 container", "test2_2/histogram" using 1:2 with line title "3 containers", "test3_2/histogram" using 1:2 with line title "5 containers", "test4_2/histogram" using 1:2 with line title "7 containers"
