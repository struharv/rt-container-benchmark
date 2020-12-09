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
	long int retCode = syscall(335, 12);
	printf("Syscall returned: %ld\n", retCode);
}

void job(int repeat) {
	for(int i = 0; i < repeat ;i++) {	
		//printf("hi, %d\n", i);
		//sleep(1); 
	}
	
}

void measure(){
	

	job(10000);
}

int main(int argc, char *argv[]) {
	struct sched_param param;
	int i;
		

	param.sched_priority = strtol(argv[1], NULL, 10);
	pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);
	display_thread_sched_attr("Scheduler settings of main thread");
	printf("\n");
	while(1) {
		markStart();	
		for(i = 0; i < 10000 ;i++) {	
			//printf("hi, %d\n", i);
			//sleep(1); 
		}
		
		usleep(1000000);
	}	


	exit(EXIT_SUCCESS);
} 
