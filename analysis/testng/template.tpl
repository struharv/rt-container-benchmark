global counter



global last = -1
global overhead = 0


#GLOBALS

probe begin 
{
	printf("Start %lu\n", gettimeofday_ns());

}

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

	if (last != -1) {	
#CONDITIONS		
		
	}
}
