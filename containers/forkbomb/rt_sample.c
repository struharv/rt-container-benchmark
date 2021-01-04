#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <time.h>
#include <sys/types.h> 
 

#include <sys/syscall.h>
#include <unistd.h>
#include <sys/time.h>

#define handle_error_en(en, msg) \
	do { errno = en; perror(msg); exit(EXIT_FAILURE); } while (0)

unsigned long timenow() {
	struct timeval timecheck;
	gettimeofday(&timecheck, NULL);
	return timecheck.tv_sec * 1000000 + (long)timecheck.tv_usec;
}

static void display_sched_attr(int policy, struct sched_param *param) {
	printf("policy=%s, priority=%d\n",
		(policy == SCHED_FIFO)  ? "SCHED_FIFO" :
		(policy == SCHED_RR)    ? "SCHED_RR" :
		(policy == SCHED_OTHER) ? "SCHED_OTHER" :
		"???",

	param->sched_priority);
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

void markEnd() {
	long int retCode = syscall(435);
	printf("return: %d\n", retCode);
}

int main(int argc, char *argv[]) {
	struct sched_param param;
	int i;
		
	
	param.sched_priority = strtol(argv[1], NULL, 10);
	pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);
 
	display_thread_sched_attr("");
    for(i = 0; i < 100; i++) { 
       if (fork() == 0) {
		printf("y\n");
		while(1) { }
		exit(0);
	}     
    }
     printf("x");

	while(1) { }
 
} 
