#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <time.h>
#include <stdio.h>
#include <linux/kernel.h>
#include <stdlib.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <sys/time.h>


#define handle_error_en(en, msg) \
	do { errno = en; perror(msg); exit(EXIT_FAILURE); } while (0)

static void display_sched_attr(int policy, struct sched_param *param) {
	printf("policy=%s, priority=%d\n",
		(policy == SCHED_FIFO)  ? "SCHED_FIFO" :
		(policy == SCHED_RR)    ? "SCHED_RR" :
		(policy == SCHED_OTHER) ? "SCHED_OTHER" :
		"???",

	param->sched_priority);
}

unsigned long timenow() {
	struct timeval timecheck;
	gettimeofday(&timecheck, NULL);
	return timecheck.tv_sec * 1000000 + (long)timecheck.tv_usec;
}



static void display_thread_sched_attr(char *msg) {
	int policy, s;
	struct sched_param param;

	s = pthread_getschedparam(pthread_self(), &policy, &param);
	if (s != 0)
		handle_error_en(s, "pthread_getschedparam");
	
	printf("%s\n", msg);
	display_sched_attr(policy, &param);
}

void markStart() {
	long int retCode = syscall(434);
}

void markEnd() {
	long int retCode = syscall(435);
}



unsigned long job(int steps){
	unsigned long start, end;
	start = timenow();	
	
	for(int i = 0; i < steps; i++) {	
		// job
	}

	end = timenow();	
	return end - start;
}


unsigned long measureMultiple(int repeat, int steps) {
	unsigned long sum = 0;	
	for (int i = 0; i < repeat; i++) {
		unsigned long duration = job(steps);
		sum += duration;		
		printf("duration: %lu\n", duration);
	}
	return sum / repeat;	
}

//1000000 loops = 2322 us
//10000000 loops = 22532 us
//100000000 loops = 221987 us


int main(int argc, char *argv[]) {	
	struct sched_param param;
	int i;
	
	int steps = 3*100000000;  
	
	param.sched_priority = 20;
	pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);
	display_thread_sched_attr("Scheduler settings of main thread\n");
	
	while(1) {
		unsigned long start = timenow();		
		
		markStart();	
		unsigned int duration = job(steps);
		markEnd();

		printf("done: %d (%ld) \n", duration, timenow() - start);
		
		unsigned long start1 = timenow();		
		
		sched_yield();	
		//usleep(1000);

		unsigned long end = timenow();		
			
		printf("\t work %ld \n", end - start);
		printf("\t yield %ld \n", end - start1);
	}

	exit(EXIT_SUCCESS);
} 
