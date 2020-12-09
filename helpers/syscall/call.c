#include <stdio.h>
#include <linux/kernel.h>
#include <stdlib.h>
#include <sys/syscall.h>
#include <unistd.h>

int main(void) {
	long int retCode = syscall(335);
	printf("Syscall returned: %ld\n", retCode);
	return EXIT_SUCCESS;
}