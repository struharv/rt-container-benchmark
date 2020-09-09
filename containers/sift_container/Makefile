build:
	g++ src/feature_extract.cpp src/wrapper.h src/wrapper.c src/common.h src/ezsift.h src/ezsift.cpp src/image.h src/image_utility.h src/image_utility.cpp src/timer.h src/vvector.h -lrt -pthread -o sift
docker:
	docker build -f Dockerfile -t struharv:sift .
	
