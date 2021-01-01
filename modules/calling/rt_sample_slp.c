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


void markStart() {
	long int retCode = syscall(434);
	printf("Syscall returned: %ld\n", retCode);
}

void markEnd() {
	long int retCode = syscall(435);
	printf("Syscall returned: %ld\n", retCode);
}

void change() {
	pid_t pid = 0;
	long int retCode = syscall(436, pid);
	printf("Syscall returned: %ld (pid = %d)\n", retCode, pid);
}

int main(int argc, char *argv[]) {	
			
	change();
	change();	
	while(1) {
		
		

	}		
	exit(EXIT_SUCCESS);
} 
