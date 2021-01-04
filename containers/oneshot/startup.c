#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>


int main(int argc, char *argv[]) {
	printf("starting\n");
	
	if (rename("rt_sample", argv[1]) == 0){
        	printf("File renamed successfully.\n");
		
		char *args[2];
		args[0] = (char *)malloc(20);
		args[1] = (char *)malloc(20);

		strcpy(args[0], argv[1]);
		strcpy(args[1], argv[2]);		
		
		char runme[20];
		sprintf(runme, "./%s", argv[1]);

		execvp(runme, args);
	} else {
		printf("NOT renamed");
	}
	
	return 0;
}