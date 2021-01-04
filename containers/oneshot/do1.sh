for i in {1..1000}
do
   sudo docker run -it --ulimit rtprio=99 --cap-add=ALL --privileged --cpu-rt-runtime=10000 --cpu-rt-period=30000  struharv:oneshot | tee -a res2
done
