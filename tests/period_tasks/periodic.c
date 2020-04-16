#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <sys/time.h>
#include <unistd.h>

#define THREADS 1




struct thread_info {    /* Used as argument to thread_start() */
	pthread_t thread_id;       
	int       id;      
	int execution_time;
	int period;     
};

unsigned long get_time_now() {
	struct timeval start;
	gettimeofday(&start, NULL);
	
	return start.tv_sec * 1000000 + start.tv_usec; 
}



static void display_thread_sched_attr() {
	int policy, s;
	struct sched_param param;

	s = pthread_getschedparam(pthread_self(), &policy, &param);
	if (s != 0)
		fprintf(stderr, "pthread_getschedparam");
	
	printf("policy=%s, priority=%d\n",
		(policy == SCHED_FIFO)  ? "SCHED_FIFO" :
		(policy == SCHED_RR)    ? "SCHED_RR" :
		(policy == SCHED_OTHER) ? "SCHED_OTHER" :
		"???",

	param.sched_priority);
}


static void * thread_start(void *arg) {
	struct thread_info *tinfo = arg;
	unsigned long start, stop;
	
	struct sched_param param;
	unsigned long counter;	
	

	printf("tick id = %d\n", tinfo->id);	
	param.sched_priority = 10;
	pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);
	display_thread_sched_attr();

	while (1) {
		start = get_time_now();
 		counter = 0;
		while (1) {		
			if ( (stop = get_time_now()) - start >= tinfo->execution_time) {
				break;			
			}
			counter++;
			//if (counter == 22000) {
			// break;
			//}
		}
		printf("start id = %d, execution = %lu, start = %lu, stop = %lu, counter = %lu \n", tinfo->id, (stop-start), start, stop, counter);
		usleep(tinfo->period);
	}

	return NULL;
}


int main(void) {
	struct thread_info thread_info[THREADS];
	
	int i;	
	for (i = 0; i < THREADS; i++) {
		thread_info[i].thread_id = (pthread_t)malloc(sizeof(pthread_t));
	}

	thread_info[0].id = 0;
	thread_info[0].execution_time = 500000;
	thread_info[0].period = 1000000;

	//thread_info[1].id = 1;
	//thread_info[1].execution_time = 500000;
	//thread_info[1].period = 1000000;

	
	printf("start\n");

	for (i = 0; i < THREADS; i++) {
		if (pthread_create(&thread_info[i].thread_id, NULL, thread_start, &thread_info[i])) {
			fprintf(stderr, "Error creating thread\n");
			return 1;
		}
	
	}
	
	for (i = 0; i < THREADS; i++) {
		pthread_join(thread_info[i].thread_id, NULL);
	}
	
	return 0;
}