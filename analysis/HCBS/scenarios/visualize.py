from PIL import Image, ImageDraw
import sys

class Result:
	def __init__(self):
		self.raw_data = []
		self.proc_info= {}		
	
	def load_file(self, filename):
		self.raw_data = []		
		
		f = open(filename, "r")
		for line in f:
			line = line.strip()
			if line <> "":			
				tmp = line.split()
	
				vect = [tmp[0], int(tmp[1]), long(tmp[2]), tmp[3]]	

				self.raw_data +=  [vect]
				self.proc_info[int(tmp[1])] = tmp[3]  
				
		f.close()
	
	def all_processes(self):
		dict = {}	
		for r in self.raw_data:
			id = r[1]
			state = r[0]
			time = long(r[2])
			name = r[3]
			
			if dict.has_key(id):
				if state == "ON":
					dict[id]["preempt"] = dict[id]["preempt"] + 1
					dict[id]["lastOn"] = time

				if state == "OFF":
					if dict[id]["lastOn"] != -1:
						dict[id]["sum"] += (time-dict[id]["lastOn"])					
			else:
				dict[id] = {"name": name, "preempt": 0, "lastOn": -1, "sum": 0}
				if state == "ON":
					dict[id]["lastOn"] = time	
		
				
		return dict
	
	def print_procesess(self, dict):
		for item in dict.items():
     			print "%s %d %d" % (item[1]["name"], item[1]["sum"], item[1]["preempt"])
	

	def metrics(self):
		start = -1
		end = -1
		
		for r in self.raw_data:
			id = r[1]
			state = r[0]
			time = long(r[2])
			name = r[3]
			
			
			if state == "ON":
				if start == -1:
					start = time
			if state == "OFF":
				end = time


		return (start, end)
		


	def analyse_timingf(self, filename, process):
		start = -1
		cnt = 0
		i = 0

		sum_time = 0
		
		for r in self.raw_data:
			id = r[1]
			state = r[0]
			time = long(r[2])
			name = r[3]
			
			if name == process:
				if state == "ON":				
					start = time

				if state == "OFF":
					if start != -1:					
						sum_time += (time-start)
						cnt += 1;
					
		return (sum_time, cnt)


		


	def getRawData(self):
		return self.raw_data
			


def simple():
	for scenario in ["scenario5.txt"]:
		res = Result() 
		res.load_file(scenario)
		metrics = res.metrics()
		#res.print_procesess(res.all_processes())
		all = res.all_processes()
		sum = 0
		for item in all.items():
			sum += item[1]["preempt"]
		print sum


		total = metrics[1]-metrics[0]
		rt_time = res.analyse_timingf("result", "rt_sample")
		#nrt_time = res.analyse_timingf("result", "rt_sampleNR")
		print scenario 
		print "rt: %d   (%2.4f) preemptions: %d" % (rt_time[0], (100.0 * rt_time[0])/total, rt_time[1])
		#print "nrt: %d   (%2.4f) preemptions: %d" % (nrt_time[0], (100.0 * nrt_time[0])/total, nrt_time[1])


def multiple(filename):
	res = Result() 
	res.load_file(filename)
	#res.print_procesess(res.all_processes())
	all = res.all_processes()
	sum = 0
	for item in all.items():
		sum += item[1]["preempt"]
	print sum

	metrics = res.metrics()
	total = metrics[1]-metrics[0]
	print total

	rt_time = res.analyse_timingf("result", "rt_sample")
	rt_time1 = res.analyse_timingf("result", "rt_sample1")
	nrt_time = res.analyse_timingf("result", "rt_sampleNR")

	print "scenario2_1"
	print "rt: %d   (%2.4f) preemptions: %d" % (rt_time[0], (100.0 * rt_time[0])/total, rt_time[1])
	print "rt1: %d   (%2.4f) preemptions: %d" % (rt_time1[0], (100.0 * rt_time1[0])/total, rt_time1[1])
	print "nrt: %d   (%2.4f) preemptions: %d" % (nrt_time[0], (100.0 * nrt_time[0])/total, nrt_time[1])



def multiple(filename):
	res = Result() 
	res.load_file(filename)
	#res.print_procesess(res.all_processes())
	all = res.all_processes()
	sum = 0
	for item in all.items():
		sum += item[1]["preempt"]
	print sum

	metrics = res.metrics()
	total = metrics[1]-metrics[0]
	print total

	rt_time = res.analyse_timingf("result", "rt_sample")
	rt_time1 = res.analyse_timingf("result", "rt_sample1")
	nrt_time = res.analyse_timingf("result", "rt_sampleNR")

	print "scenario2_1"
	print "rt: %d   (%2.4f) preemptions: %d" % (rt_time[0], (100.0 * rt_time[0])/total, rt_time[1])
	print "rt1: %d   (%2.4f) preemptions: %d" % (rt_time1[0], (100.0 * rt_time1[0])/total, rt_time1[1])
	print "nrt: %d   (%2.4f) preemptions: %d" % (nrt_time[0], (100.0 * nrt_time[0])/total, nrt_time[1])



def multiplex(filename):
	res = Result() 
	res.load_file(filename)
	#res.print_procesess(res.all_processes())
	all = res.all_processes()
	sum = 0
	for item in all.items():
		sum += item[1]["preempt"]
	
	metrics = res.metrics()
	total = metrics[1]-metrics[0]
	
	rt_time = res.analyse_timingf("result", "rt_sample")
	rt_time1 = res.analyse_timingf("result", "rt_sample1")
	nrt_time = res.analyse_timingf("result", "rt_sampleNR")

	overhead = 100-100*(rt_time[0] + rt_time1[0] + nrt_time[0])/float(total)

	print "overhead: %2.6f" % overhead
	rt1 = (100.0 * rt_time[0])/float(total)
	rt2 = (100.0 * rt_time1[0])/float(total)
	nrt = (100.0 * nrt_time[0])/float(total)	
	print "%2.4f %2.4f %2.4f" % (rt1, rt2, nrt)
	
def multiplex3(filename):
	res = Result() 
	res.load_file(filename)
	#res.print_procesess(res.all_processes())
	all = res.all_processes()
	sum = 0
	for item in all.items():
		sum += item[1]["preempt"]
	
	metrics = res.metrics()
	total = metrics[1]-metrics[0]
	
	rt_time = res.analyse_timingf("result", "rt_sample")
	rt_time1 = res.analyse_timingf("result", "rt_sample1")
	rt_time2 = res.analyse_timingf("result", "rt_sample2")
	nrt_time = res.analyse_timingf("result", "rt_sampleNR")

	overhead = 100-(100*(rt_time[0] + rt_time1[0] + rt_time2[0] + nrt_time[0])/total)

	print "overhead: %2.5f" % overhead
	print "rt: %d   (%2.5f) preemptions: %d" % (rt_time[0], (100.0 * rt_time[0])/total, rt_time[1])
	print "rt1: %d   (%2.5f) preemptions: %d" % (rt_time1[0], (100.0 * rt_time1[0])/total, rt_time1[1])
	print "rt2: %d   (%2.5f) preemptions: %d" % (rt_time2[0], (100.0 * rt_time2[0])/total, rt_time2[1])
	print "nrt: %d   (%2.5f) preemptions: %d" % (nrt_time[0], (100.0 * nrt_time[0])/total, nrt_time[1])

def analyse_all():
	rt1 = [4000]
	rt2 = [200, 500, 1000, 2000, 3000, 4000, 5000, 5500]


	for irt1 in rt1:
		for irt2 in rt2:
			print "%d %d" % (irt1, irt2)
			filename = "test_%d_%d.tst" % (irt1, irt2)
			multiplex(filename)


	

def analyse3():
	multiplex3("test3_50000_50000_50000.tst")	
	multiplex3("test3_100000_100000_100000.tst")	
	multiplex3("test3_200000_200000_200000.tst")
	multiplex3("test3_250000_250000_250000.tst")
	
	

#multiplex("testPeriod_[100000, 1000000]_[100000, 1000000].tst")
#multiplex("testPeriod_[100000, 1000000]_[100000, 1000000].tst")
#multiplex("testPeriod_[100000, 2000000]_[100000, 1000000].tst")
#multiplex("testPeriod_[100000, 500000]_[100000, 3000000].tst")



#analyse3()
#analyse_all()