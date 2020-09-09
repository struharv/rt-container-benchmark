#include <unistd.h>
#include <linux/unistd.h>
#include <linux/types.h>
#include <pthread.h>
#include <signal.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <linux/sched.h>

#define gettid() syscall(__NR_gettid)

#define SCHED_DEADLINE  6

/* XXX use the proper syscall numbers */
#ifdef __x86_64__
#define __NR_sched_setattr      314
#define __NR_sched_getattr      315
#endif

#ifdef __i386__
#define __NR_sched_setattr      351
 #define __NR_sched_getattr     352
#endif

#ifdef __arm__
#define __NR_sched_setattr      380
 #define __NR_sched_getattr     381
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

int main (void) {
    printf("MY PID: %d\n", getpid());
    set_rt(gettid(), 500000Ul, 1000000000Ul, 1000000000Ul);

    struct sigaction s;
    bzero(&s, sizeof(s));
    s.sa_handler = sig_handler;
    sigaction (SIGXCPU, &s, NULL);

    //test signal handler
    //kill(getpid(), SIGXCPU);

    int i = 0;
    while (1) {
        i++;
        printf("Loop Number %d\n", i);
        int k = 900000000;
        if (i == 3) {
            while (k > 0) k--;
        }
        sched_yield();
    }
}
