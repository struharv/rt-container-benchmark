import subprocess
import time
import glob
import os
import visualizeme

#import visualize


prefix = "/sys/fs/cgroup/cpu,cpuacct/docker"
rt1_name = prefix + "/6e7415fc751d2c2a043032b382d541ac006c39fca303cd68528bb705a1fa8c72"
rt2_name = prefix + "/2569ec65850cc0bc6063c2b596d2a71f9428f304038a36481416b7a77deedac1"
rt3_name = prefix + "/a5974d1cb7404b693c4c9a8f6bafd138025fbe66e85bdeaddcd01c3ef45c4a1d"




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
		command = "stap process_monitor.stp -T %d > '%s'" % (time, file_name)
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
	

	def runrtcontainer(self, name, period, runtime):
		command =  "docker run -it --ulimit rtprio=99 --cap-add=sys_nice --cpu-rt-runtime=%d struharv:dummy ./startup %s 85 " % (runtime, name)	
		self.run(command)
		time.sleep(1)
		cont_dir = self.last_container_dir()
		self.write_period(cont_dir, period)
		return cont_dir

	def runcontainer(self, name):
		command =  "docker run -it struharv:dummy ./startup %s 85 " % (name)	
		self.run(command)
		time.sleep(1)
		return self.last_container_dir()

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
		
		for rtc in rtContainers:
			self.runrtcontainer(rtc[0], rtc[1], rtc[2])
			print rtc 


		for c in containers:
			self.runcontainer(c)
			print c 
			time.sleep(5)	
		
		self.stap(filename, 40)
		self.killall()
	
	def allcontainers(self, rtContainers, containers):
		res = []
		for rt in rtContainers:
			res += [rt[0]]
		for c in containers:
			res += [c]

		return res

	def printx(self, visualizedata, containers):
		for item in visualizedata["data"]:
			print item["name"], 100*item["stats"][0]/float(visualizedata["total"])
		print "overhead", 100*(1-visualizedata["overhead"]/float(visualizedata["total"]))
			 
	
def scenario1(filename, run=False):
	overheads = [];
	for i in range(0, 20, 2):
		realname = filename % i		
		tst = DockerTester()		
		
		rtcontainers = [("rt_sample1", 100000, 30000)]
		containers = []		
		for j in range(i):
			containers += [("nr%d" % j)]	
		if run:	
			print "RUNNING"
			tst.scenario(1000000, 900000, rtcontainers, containers, realname)
		
		data = visualizeme.analyse(realname, tst.allcontainers(rtcontainers, containers))
		tst.printx(data, tst.allcontainers(rtcontainers, containers));
		overheads += [data["overhead"]/float(data["total"])]
		
	return overheads


def scenario1_faster(filename, run=False):
	overheads = [];
	for i in range(0, 20, 2):
		realname = filename % i		
		tst = DockerTester()		
		
		rtcontainers = [("rt_sample1", 10000, 3000)]
		containers = []		
		for j in range(i):
			containers += [("nr%d" % j)]	
		if run:	
			print "RUNNING"
			tst.scenario(1000000, 900000, rtcontainers, containers, realname)
		
		data = visualizeme.analyse(realname, tst.allcontainers(rtcontainers, containers))
		tst.printx(data, tst.allcontainers(rtcontainers, containers));
		overheads += [data["overhead"]/float(data["total"])]
		
	return {"overheads": overheads, "data": data}

def scenario1_vfaster(filename, run=False):
	overheads = [];
	for i in range(0, 20, 2):
		realname = filename % i		
		tst = DockerTester()		
		
		rtcontainers = [("rt_sample1", 1000, 300)]
		containers = []		
		for j in range(i):
			containers += [("nr%d" % j)]	
		if run:	
			print "RUNNING"
			tst.scenario(1000000, 900000, rtcontainers, containers, realname)
		
		data = visualizeme.analyse(realname, tst.allcontainers(rtcontainers, containers))
		tst.printx(data, tst.allcontainers(rtcontainers, containers));
		overheads += [data["overhead"]/float(data["total"])]
		
	return {"overheads": overheads, "data": data}		


def scenario2(filename):
	for i in range(0, 9):
		realname = filename % i		
		tst = DockerTester()
		rtcontainers = []		
		for j in range(i):
			rtcontainers += [("rt_sample%d" % j, 100000, 10000)]
		
		containers = [("nr")]	

		tst.scenario(1000000, 900000, rtcontainers, containers, realname)
		data = visualizeme.analyse(realname, tst.allcontainers(rtcontainers, containers))
		tst.printx(data, tst.allcontainers(rtcontainers, containers));


def scenario3(filename):
	for i in range(0, 9):
		realname = filename % i		
		tst = DockerTester()
		rtcontainers = []		
		for j in range(i):
			rtcontainers += [("rt_sample%d" % j, 10000, 1000)]
		
		containers = [("nr")]	

		tst.scenario(1000000, 900000, rtcontainers, containers, realname)
		data = visualizeme.analyse(realname, tst.allcontainers(rtcontainers, containers))
		tst.printx(data, tst.allcontainers(rtcontainers, containers));



def scenario4(filename):
	for i in range(0, 10):
		realname = filename % i		
		tst = DockerTester()
		rtcontainers = []		
		for j in range(i):
			rtcontainers += [("rt_sample%d" % j, 1000, 100)]
		
		containers = [("nr")]	

		tst.scenario(1000000, 900000, rtcontainers, containers, realname)
		data = visualizeme.analyse(realname, tst.allcontainers(rtcontainers, containers))
		tst.printx(data, tst.allcontainers(rtcontainers, containers));



def scenario5(filename):
	for i in range(0, 20):
		realname = filename % i		
		tst = DockerTester()
		rtcontainers = []		
		for j in range(i):
			rtcontainers += [("rt_sample%d" % j, 100000, 5000)]
		
		containers = [("nr")]	

		tst.scenario(1000000, 900000, rtcontainers, containers, realname)
		data = visualizeme.analyse(realname, tst.allcontainers(rtcontainers, containers))
		tst.printx(data, tst.allcontainers(rtcontainers, containers));


#scenario5("tst%d_5.txt")


#for i in range(50):
#	scenario1("tst%d.txt_"+str(i))
#	scenario2("tst%d_2.txt_"+str(i))
#	scenario3("tst%d_3.txt_"+str(i))
#	scenario4("tst%d_4.txt_"+str(i))
#	scenario5("tst%d_5.txt_"+str(i))



#scenario1_vfaster("tst_vfaster%d.txt_0", True)
#scenario1_faster("tst_faster%d.txt_1")


scenario1_vfaster("tst_vfaster%d.txt_0")


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




