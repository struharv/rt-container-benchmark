global counter



global last = -1
global overhead = 0
global ok = 0

#GLOBALS



probe end 
{	printf("Overhead %d\n", overhead);
	#PRINTS	
	printf("End %lu\n", gettimeofday_ns());
	printf("Preemptions %d\n", counter)
}

probe scheduler.cpu_on
{
	counter = counter +1;
    	last = gettimeofday_ns()
	
}

probe scheduler.cpu_off
{	
	if (ok == 0 && isinstr(execname(), "stress-ng")) {
		printf("Start %lu\n", gettimeofday_ns());		
		ok = 1;
		printf("stress-ng!\n");
		
	}	
	if (last != -1 && ok == 1) {	
#CONDITIONS		
		
	}
}
