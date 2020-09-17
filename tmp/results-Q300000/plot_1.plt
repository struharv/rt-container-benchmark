set title "Latency plot"
set terminal png
set xlabel "Latency (us)"
set logscale y
set xrange [0:600]
set yrange [0.8:*]
set ylabel "Number of latency samples"
set output "plot.png"
plot "result1/histogram" using 1:2 with line title "1 rt, 0 sift", "result1-sift/histogram" using 1:2 with line title "31 rt, 1 sift", "result1-sift2/histogram" using 1:2 with line title "1 rt, 2 sift", "result1-sift3/histogram" using 1:2 with line title "1 rt, 3 sift", "result1-sift4/histogram" using 1:2 with line title "1 rt, 4 sift", "result1-sift5/histogram" using 1:2 with line title "1 rt, 5 sift" 
