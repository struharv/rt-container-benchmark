sudo docker run -it --cpu-rt-runtime=900000 --ulimit rtprio=99 --cap-add=sys_nice struharv:edf_test
