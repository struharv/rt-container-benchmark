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
		command = "python ../stap-generator.py %s > stap_script.stp"		
		
		arg = ""		
		for p in processes:
			arg +=p+" "
		command = command % arg
		print(command)
		self.runwait(command)


	def runrtcontainer(self, name, period, runtime):
		command =  "docker run -it --ulimit rtprio=99 --cap-add=sys_nice --cpu-rt-runtime=%d --cpu-rt-period=%d  struharv:dummy ./startup %s 85 " % (runtime, period, name)	
		self.run(command)
		time.sleep(20)
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



#i = 0
#scenario("results/xscenario1_nr%%d_%d.txt"  % i, makeRT(1, 100000, 10000), 1000000, 900000, True)
#scenario("results/xscenario2_nr%%d_%d.txt"  % i, makeRT(3, 100000, 10000), 1000000, 900000, True)
#scenario("results/xscenario3_nr%%d_%d.txt"  % i, makeRT(5, 100000, 10000), 1000000, 900000, True)
#scenario("results/xscenario4_nr%%d_%d.txt"  % i, makeRT(7, 100000, 10000), 1000000, 900000, True)


#
#i=0
for i in range(5):
	scenario("results/scenario1/scenario1_nr%%d_%d.txt"  % i, [("rt_sample1", 10000, 1000)], 1000000, 900000, True)
	scenario("results/scenario2/scenario2_nr%%d_%d.txt" % i, [("rt_sample1", 100000, 10000)], 1000000, 900000, True)
	scenario("results/scenario3/scenario3_nr%%d_%d.txt" % i, [("rt_sample1", 1000000, 100000)], 1000000, 900000, True)


for i in range(5):
	scenario("results/xscenario1_nr%%d_%d.txt"  % i, makeRT(1, 100000, 10000), 1000000, 900000, True)
	scenario("results/xscenario2_nr%%d_%d.txt"  % i, makeRT(3, 100000, 10000), 1000000, 900000, True)
	scenario("results/xscenario3_nr%%d_%d.txt"  % i, makeRT(5, 100000, 10000), 1000000, 900000, True)
	scenario("results/xscenario4_nr%%d_%d.txt"  % i, makeRT(7, 100000, 10000), 1000000, 900000, True)









#scenario3("results/tst%d.txt_"+str(1), True)

#for i in range(50):
#	scenario1("tst%d.txt_"+str(i))
#	scenario2("tst%d_2.txt_"+str(i))
#	scenario3("tst%d_3.txt_"+str(i))
#	scenario4("tst%d_4.txt_"+str(i))
#	scenario5("tst%d_5.txt_"+str(i))



'''

def analyse(pattern):
	for i in range(20):
		tmp = (pattern % i) 
		tmp = tmp.replace("#", "%")
		for j in range(5):
			name = tmp % j
			print name, os.path.isfile(name) 


data = []
data += [scenario1("tst%d.txt_5")]
#data += scenario1("tst%d.txt_6")
#data += scenario1("tst%d.txt_7")
#data += scenario1("tst%d.txt_8")


total = []
rt = []

print data[0]
print "\n"

print data
dpoints = len(data[0])
for j in range(dpoints):
	sum = 0
	sumrt = 0
	for i in range(4):		
		sum += data[i][j]
		
		 
	total += [100 * (1 - (sum / 4.0))]




	

print total
'''




