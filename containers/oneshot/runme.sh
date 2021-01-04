docker run -it --ulimit rtprio=99 --cap-add=ALL --cpu-rt-runtime=500000 --cpu-rt-period=1000000  struharv:oneshot
