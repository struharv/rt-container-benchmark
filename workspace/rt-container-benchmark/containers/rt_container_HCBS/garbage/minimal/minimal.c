#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


int main(int argc, char *argv[]) {
	struct sched_param param;
	
	param.sched_priority = 20;
	pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);

	// now this process is scheduled by FIFO and has priority 20

	exit(EXIT_SUCCESS);
} 
