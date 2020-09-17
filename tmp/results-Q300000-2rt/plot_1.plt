set title "Latency plot"
set terminal png
set xlabel "Latency (us)"
set logscale y
set xrange [0:600]
set yrange [0.8:*]
set ylabel "Number of latency samples"
set output "plot.png"
plot "result1/histogram" using 1:2 with line title "1 rt container", "result1-1/histogram" using 1:2 with line title "2 rt containers", "result1-2/histogram" using 1:2 with line title "3 rt containers"