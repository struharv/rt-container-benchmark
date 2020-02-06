sudo docker run -it --cpu-rt-runtime=50000 --ulimit rtprio=99 --cap-add=sys_nice struharv:edf
