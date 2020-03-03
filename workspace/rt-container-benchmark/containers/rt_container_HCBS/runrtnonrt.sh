docker run --cpu-rt-runtime=400000 --ulimit rtprio=99 --cap-add=sys_nice struharv:rt &
docker run --cpu-rt-runtime=100000 --ulimit rtprio=99 --cap-add=sys_nice struharv:rt1 &
docker run struharv:nrt &
