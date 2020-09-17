
cnt=6
name=XX12

for i in `seq 1 $cnt`
do
	sudo docker run -it --name "$name"_"$i" --ulimit rtprio=99 --cap-add=sys_nice --cpu-rt-runtime=20000 --cpu-rt-period=100000  struharv:cyclic /bin/cyclictest -l500000 -Sp90 -i100 -h600 -q	
	sudo docker logs "$name"_"$i" > cyclic_$i.res
done
