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

#define SCHED_DEADLINE  6

/* XXX use the proper syscall numbers */
#ifdef __x86_64__
#define __NR_sched_setattr      314
#define __NR_sched_getattr      315
#endif
#ifdef __i386__
#define __NR_sched_setattr      351
#define __NR_sched_getattr      352
#endif
#ifdef __arm__
#define __NR_sched_setattr      380
#define __NR_sched_getattr      381
#endif

 static volatile int done;

 struct sched_attr {
     __u32 size;

     __u32 sched_policy;
     __u64 sched_flags;

     /* SCHED_NORMAL, SCHED_BATCH */
     __s32 sched_nice;

     /* SCHED_FIFO, SCHED_RR */
     __u32 sched_priority;

     /* SCHED_DEADLINE (nsec) */
     __u64 sched_runtime;
     __u64 sched_deadline;
     __u64 sched_period;
 };


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

 int sched_setattr(pid_t pid, const struct sched_attr *attr, unsigned int flags)
 {     return syscall(__NR_sched_setattr, pid, attr, flags);
 }

 int sched_getattr(pid_t pid, struct sched_attr *attr, unsigned int size, unsigned int flags)
 {
     return syscall(__NR_sched_getattr, pid, attr, size, flags);
 }

//1000000 loops = 2322 us
//10000000 loops = 22532 us
//100000000 loops = 221987 us


int main(int argc, char *argv[]) {	
	struct sched_param param;
	int i;
	
	int steps = 3*100000000; 
 
	struct sched_attr attr;
	attr.size = sizeof(attr);
     	attr.sched_flags = 0;
	attr.sched_nice = 0;
	attr.sched_priority = 0;

     	attr.sched_policy = SCHED_FIFO;
	attr.sched_priority = 21;
	
	sched_setattr(0, &attr, 0);	
	//pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);

	display_thread_sched_attr("Scheduler settings of main thread\n");
	
	while(1) {
		unsigned long start = timenow();		
		
		markStart();	
		unsigned int duration = job(steps);
		markEnd();

		printf("done: %d (%ld) \n", duration, timenow() - start);
		
		unsigned long start1 = timenow();		
		
		sched_yield();	
		usleep(1000);

		unsigned long end = timenow();		
			
		printf("\t work %ld \n", end - start);
		printf("\t yield %ld \n", end - start1);
	}

	exit(EXIT_SUCCESS);
} 
