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
#include <stdint.h>
#include <sys/time.h>
#include <signal.h>
#include <semaphore.h>

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


unsigned long long userspace;
unsigned long long kernelspace;

static sem_t event_sem;
static volatile sig_atomic_t interested = 0;

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


struct struhar_attr {
     __u64 period;
     __u64 now;
     char test;
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

void sig_handler(int sig) {
	interested = 1;
	sem_post(&event_sem);
	printf("SIGNAL received: %d\n", sig);
}



unsigned long timenow() {
	struct timeval timecheck;
	gettimeofday(&timecheck, NULL);
	return timecheck.tv_sec * 1000000 + (long)timecheck.tv_usec;
}

unsigned long long ktime() {
	return syscall(437);
}

unsigned long long updateNow() {
	kernelspace = ktime();
	userspace = timenow();
	
	printf("NOW: %llu %lu\n", kernelspace, userspace);
	return ktime;
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
	syscall(434);
}

void markEnd() {
	syscall(435);
}

void startTimer() {
	syscall(434);
}


unsigned long long next_period() {
	struct struhar_attr attr;
	unsigned long *a, *b;
	a = (unsigned long *)malloc(sizeof(unsigned long));
	b = (unsigned long *)malloc(sizeof(unsigned long));
	*a = 12;
	
	
	unsigned long long ret = syscall(436, a, b, 8);
	return ret;
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


void *worker(void *x_void_ptr) {
	//struct sched_param param;
	int id = (int)(x_void_ptr);	
	
	//int steps = 3*10000000; 
 
	struct sched_attr attr;
	attr.size = sizeof(attr);
     	attr.sched_flags = 0;
	attr.sched_nice = 0;
	attr.sched_priority = 0;

     	attr.sched_policy = SCHED_FIFO;
	attr.sched_priority = 12;
	
	sched_setattr(0, &attr, 0);	
	display_thread_sched_attr("XXX");
	//pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);
	
	//updateNow();
	
	//markStart();
	//while(1) {
		//printf("start\n");
		//long elapsed = job(100);
		//printf("elapsed: %d %d \n", elapsed, id);
		//startTimer();
		//sem_wait(&event_sem);		
		//pthread_yield();
		//startTimer();
		//printf("yield \n");

		//sleep(1);
	//}
	printf("hey\n");	

	printf("hou\n");
	while(1) {
		long elapsed = job(100000);
		printf("elapsed: %d %d \n", elapsed, id);
		startTimer();
		
		while (interested == 0) {
			sem_wait(&event_sem);
		}		
		interested = 0;
			
			
	}
	
	

}


int main(int argc, char *argv[]) {	
	struct sigaction action;
	sigset_t block_mask;

	sigfillset(&block_mask);
	action.sa_handler = sig_handler;
	action.sa_mask = block_mask;
	action.sa_flags = SA_NODEFER;
	sigaction(44, &action, NULL);
	sem_init(&event_sem, 0, 0);

	pthread_t thr1, thr2;

	pthread_create(&thr1, NULL, worker, 0);
	//pthread_create(&thr2, NULL, worker, 1);
	pthread_join(thr1, NULL);
	//pthread_join(thr2, NULL);

	exit(EXIT_SUCCESS);
} 
