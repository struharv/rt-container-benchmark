g++ feature_extract.cpp wrapper.h wrapper.c common.h ezsift.h ezsift.cpp image.h image_utility.h image_utility.cpp timer.h vvector.h -lrt -pthread -o sift
cp sift ../Benchmark_tests
