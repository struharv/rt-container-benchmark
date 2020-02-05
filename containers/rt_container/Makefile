
build:
	gcc -Wall -O0 rt_sample.c -o rt_sample -pthread
docker:
	docker build -f Dockerfile -t struharv:rt .
	docker build -f Dockerfile1 -t struharv:rt1 .
	docker build -f DockerfileNR -t struharv:nrt .

