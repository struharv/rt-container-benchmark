
cnt=6
for i in `seq 1 $cnt`
do
	sudo docker run -it --name c16_$i --ulimit rtprio=99 --cap-add=sys_nice --cpu-rt-runtime=30 --cpu-rt-period=100  struharv:cyclic /bin/cyclictest -l500000 -Sp90 -i100 -h600 -q	
	sudo docker logs c16_$i > cyclic_$i.res
done
