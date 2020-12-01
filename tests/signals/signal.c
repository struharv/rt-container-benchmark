#include <unistd.h>
#include <linux/unistd.h>
#include <linux/types.h>
#include <pthread.h>
#include <signal.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <linux/sched.h>
#include <sys/time.h>

#define gettid() syscall(__NR_gettid)

#define SCHED_DEADLINE  6

/* XXX use the proper syscall numbers */
#ifdef __x86_64__
#define __NR_sched_setattr	  314
#define __NR_sched_getattr	  315
#endif

#ifdef __i386__
#define __NR_sched_setattr	  351
 #define __NR_sched_getattr	 352
#endif

#ifdef __arm__
#define __NR_sched_setattr	  380
 #define __NR_sched_getattr	 381
#endif

// 1 sec = 1000 ms = 1 000 000 us = 1 000 000 000 ns 
// 0.5 sec =	500 000 000							

#define PERIOD  100 * 1000 * 1000
#define RUNTIME 5 * 1000 * 1000

#define ENTRIES 10



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

int sched_setattr(pid_t pid,
				  const struct sched_attr *attr,
				  unsigned int flags)
{
	return syscall(__NR_sched_setattr, pid, attr, flags);
}

int sched_getattr(pid_t pid,
				  struct sched_attr *attr,
				  unsigned int size,
				  unsigned int flags)
{
	return syscall(__NR_sched_getattr, pid, attr, size, flags);
}


void set_rt(int pid, unsigned long runtime, unsigned long period, unsigned long deadline){
	struct sched_attr attr;
	unsigned int flags = 0;
	attr.size = sizeof(attr);
	attr.sched_flags =  SCHED_FLAG_DL_OVERRUN;
	attr.sched_nice = 0;
	attr.sched_priority = 0;
	attr.sched_policy = SCHED_DEADLINE;
	attr.sched_runtime = runtime;
	attr.sched_period = period;
	attr.sched_deadline = deadline;

	int ret = sched_setattr(pid, &attr, 0);
	if (ret < 0) {
		done = 0;
		perror("sched_setattr");
		exit(-1);
	}

	struct sched_attr param;
	ret = sched_getattr(pid, &param, sizeof(param), 0);
	if (ret < 0) {
		done = 0;
		perror("sched_getattr");
		exit(-1);
	}
}

void sig_handler(int signo)
{
	if (signo == SIGXCPU)
		printf("received SIGXCPU\n");
}


unsigned long get_time_now() {
	struct timeval start;
	gettimeofday(&start, NULL);
	
	return start.tv_sec * 1000000 + start.tv_usec; 
}

int loop(int cycles) {
	unsigned long start, stop;
	
	
	start = get_time_now();
	for (int i = 0; i < cycles; i++) {
		//			
	}
	stop = get_time_now();


	return stop - start;
}


void average(int attempts, int cycles) {
	int sum = 0;	

	for(int i = 0; i < attempts; i++) {
		sum += loop(cycles);
	}

	printf("%f\n", sum / (double)attempts);


}

struct entry {
	unsigned long start;
	unsigned long stop;
};

struct entry entries[100];

int main (void) {
	unsigned long start, stop;
	unsigned long sleep_time;

	printf("MY PID: %d\n", getpid());
	set_rt(gettid(), RUNTIME, PERIOD, PERIOD);
	
	struct sigaction s;
	bzero(&s, sizeof(s));
	s.sa_handler = sig_handler;
	sigaction (SIGXCPU, &s, NULL);

	//test signal handler
	//kill(getpid(), SIGXCPU);

	int cnt = 0;
	while (cnt < ENTRIES) {
		start = get_time_now();


		for (int i = 0; i < 1*1000000; i++) {
		}

		stop = get_time_now();
		sleep_time = PERIOD - (stop-start);
		entries[cnt].start = start;
		entries[cnt].stop = stop;
					
		//sched_yield();
		usleep(sleep_time / 1000);
		
		cnt++;
		printf("%ld, %ld\n", stop - start, sleep_time);
	}

	for(int i = 0; i < ENTRIES; i++) {
		printf("%lu, %lu (%ld)\n", entries[i].start, entries[i].stop, entries[i].stop - entries[i].start);
		if (i > 0) {
			printf("	%lu\n", entries[i].start-entries[i-1].start);
		}
	}
	

}
