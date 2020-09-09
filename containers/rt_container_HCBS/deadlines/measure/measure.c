#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

#define TRIES 1000 

unsigned long timenow() {
	struct timeval timecheck;
	gettimeofday(&timecheck, NULL);
	return timecheck.tv_sec * 1000000 + (long)timecheck.tv_usec;
}

int main(int argc, char *argv[]) {
	int i, y;
	unsigned long start, end, diff, sum = 0;


	for (y = 0; y < TRIES; y++) {
		start = timenow();
		for(i = 0; i < 100000000; i++) {

		}
		end = timenow();
		diff = end - start;
		sum += diff;
		printf("%lu\n", diff);
	}

	printf ("avarage = %lu\n", sum / TRIES);



	return 0;
}