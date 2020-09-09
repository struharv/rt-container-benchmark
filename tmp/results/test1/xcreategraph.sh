python tohistogram.py > histogram

echo -n -e "set title \"Latency plot\"\n\
set terminal png\n\
set xlabel \"Latency (us), max $max us\"\n\
set logscale y\n\
set xrange [0:600]\n\
set yrange [0.8:*]\n\
set ylabel \"Number of latency samples\"\n\
set output \"plot.png\"\n\
plot \"histogram\" using 1:2 title \"$title\" with line \n" > plotcmd


gnuplot -persist <plotcmd

