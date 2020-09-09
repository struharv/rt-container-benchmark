#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

long timenow() {
	struct timeval timecheck;
	gettimeofday(&timecheck, NULL);
	return (long)timecheck.tv_sec * 1000 + (long)timecheck.tv_usec / 1000;
}

int main(int argc, char *argv[]) {
	int i;
	long start, end, diff;

	
	start = timenow();
	for(i = 0; i < 100000; i++) {

	}
	end = timenow();
	diff = end - start;
	printf("%lld\n", diff);



	return 0;
}