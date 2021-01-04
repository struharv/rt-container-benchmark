import subprocess
import time
import glob
import os


#import visualize


prefix = "/sys/fs/cgroup/cpu,cpuacct/docker"


class DockerTester:
	def __init__(self):
		pass
	
	def write_runtime(self, rt_name, value):
		runtime = "%s/cpu.rt_runtime_us" % rt_name	
		f = open(runtime, "w")
		f.write(str(value))
		f.close()


	def write_period(self, rt_name, value):
		runtime = "%s/cpu.rt_period_us" % rt_name	
		f = open(runtime, "w")
		f.write(str(value))
		f.close()
	
	def stress_ng(self, time):
		command =  "sudo docker run -it --cap-add=ALL --privileged --rm alexeiled/stress-ng --cpu 30 --hdd 20 --x86syscall 20 --io 40 --link 30 --clock 30 --context 30  --vm-bytes 1G --timeout %ds --metrics-brief" % time
		self.run(command)	

	def stress_ng_rt(self, runtime, period, time):
		command =  "sudo docker run -it --cap-add=ALL --privileged --cpu-rt-runtime=%d --cpu-rt-period=%d --rm alexeiled/stress-ng --cyclic 100 --cyclic-policy fifo --metrics-brief --timeout %ds" % (runtime, period, time)
		self.run(command)	


	def stap(self, file_name, time):
		command = "stap stap_script.stp -T %d > '%s'" % (time, file_name)
		print command
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()

	def runwait(self, command):
		print command
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()

	def run(self, command):
		print command
		process = subprocess.Popen(command, shell=True)
	
	def generate_stap(self, processes):
		command = "python stap-generator.py %s > stap_script.stp"		
		
		arg = ""		
		for p in processes:
			arg +=p+" "
		command = command % arg
		print(command)
		self.runwait(command)


	def runrtcontainer(self, name, period, runtime):
		command =  "docker run -it --ulimit rtprio=99 --cap-add=sys_nice --cpu-rt-runtime=%d --cpu-rt-period=%d  struharv:dummy ./startup %s 85 " % (runtime, period, name)	
		self.run(command)
		time.sleep(5)
		cont_dir = self.last_container_dir()
		self.write_period(cont_dir, period)
		return cont_dir

	def runcontainer(self, name):
		command =  "docker run -it struharv:dummy ./startup %s 85 " % (name)	
		self.run(command)
		#time.sleep(5)
		#return self.last_container_dir()

	def killall(self):
		self.runwait("docker kill $(sudo docker ps -q)")	
 
	def last_container_dir(self):
		list_of_files = glob.glob('/sys/fs/cgroup/cpu,cpuacct/docker/*/') 
		latest_file = max(list_of_files, key=os.path.getctime)
		return latest_file 

	def scenario(self, dPeriod, dRuntime, rtContainers, containers, filename):
		global prefix
		
		self.write_period(prefix, dPeriod)
		self.write_runtime(prefix, dRuntime)
		
		
		for c in containers:
			self.runcontainer(c)
			print c 
			time.sleep(2)	
		
		for rtc in rtContainers:
			self.runrtcontainer(rtc[0], rtc[1], rtc[2])
			print rtc 
			time.sleep(2)
		

		self.generate_stap(self.allcontainers(rtContainers, containers))
		self.stap(filename, 40)
		self.killall()
		time.sleep(5)
	
	def allcontainers(self, rtContainers, containers):
		res = []
		for rt in rtContainers:
			res += [rt[0]]
		for c in containers:
			res += [c]

		return res

	def printx(self, visualizedata, containers):
		for item in visualizedata["data"]:
			print item["name"], 100*item["stats"][0]/float(visualizedata["total"]), " preemptions", item["stats"][1]
		print "overhead", 100*(1-visualizedata["overhead"]/float(visualizedata["total"]))
			 
	
def scenario(filename, rtcontainers, dockerPeriod, dockerBudget, run=False):
	overheads = [];
	for i in [10]:
		realname = filename % i		
		tst = DockerTester()		
		
		containers = []		
		for j in range(i):
			containers += [("nr%d" % j)]	
		if run:	
			print "RUNNING"
			tst.scenario(1000000, 900000, rtcontainers, containers, realname)

		
		
		#data = visualizeme.analyse(realname, tst.allcontainers(rtcontainers, containers))
		#tst.printx(data, tst.allcontainers(rtcontainers, containers));
		#overheads += [data["overhead"]/float(data["total"])]
		
	return overheads		

def makeRT(number, period, budget):
	res = []
	for i in range(number):
		res += [("rt_sample%d" % i, period, budget)]


	return res



def runRT():
	tst = DockerTester()		
	container_names = []
	
	for i in range(1):
		cname = "rtcontainer_%d" % i		
		tst.runrtcontainer(cname, 20000, 10000)
		
		container_names += [cname]
	
	for i in range(1):
		cname = "container_%d" % i		
		tst.runcontainer(cname)
		
		container_names += [cname]


	container_names += ["stress-ng"]
	tst.generate_stap(container_names)	
	tst.stress_ng_rt(10000, 30000, 200);
	time.sleep(2)
	tst.stap("result", 40)
	tst.killall()
	time.sleep(5)

		

runRT()






