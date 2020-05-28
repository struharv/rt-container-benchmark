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
			

def analyse(filename, process):
	res = Result() 
	res.load_file(filename)
	all = res.all_processes()
	sum = 0
	for item in all.items():
		sum += item[1]["preempt"]
	
	metrics = res.metrics()
	total = metrics[1]-metrics[0]
	
	output = [];
	overhead = 0
	for proc in process:
		rt_time = res.analyse_timingf("result", proc)
		overhead +=  rt_time[0]	
		output += [{"name": proc, "stats": rt_time, "preemptions": rt_time[1]}]

	return {"total": total, "data": output, "overhead": overhead}

	#overhead = 100-(100*(rt_time[0] + rt_time1[0] + rt_time2[0] + nrt_time[0])/total)
	#print "rt: %d   (%2.5f) preemptions: %d" % (rt_time[0], (100.0 * rt_time[0])/total, rt_time[1])



