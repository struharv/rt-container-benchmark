docker run -it --ulimit rtprio=99 --cap-add=ALL --cpu-rt-runtime=5000 --cpu-rt-period=10000  struharv:bomb
