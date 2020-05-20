docker run -it --ulimit rtprio=99 --cap-add=sys_nice --cpu-rt-runtime=400000 struharv:busywait
