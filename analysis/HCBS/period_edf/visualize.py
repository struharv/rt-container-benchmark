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
	
	def analyse_timingf(self, filename):
		start = -1
		cnt = 0
		i = 0

		sum_time = 0
		sum_i = 0;	
		
		f = open(filename, "w")
		for r in self.raw_data:
			id = r[1]
			state = r[0]
			time = long(r[2])
			name = r[3]
			
			
			if state == "ON":
				if name == "rt_sample":				
					if start != -1:
						#print time-start, 
						sum_time += (time-start)
						sum_i += 1						
						f.write("%d %d\n" % (cnt, (time-start)))
						cnt += 1						
					
					start = time

							#elif state=="OFF" and i != 0:
			#	if name == "rt_sample" :
			#		cnt += 1		
			#		f.write("%d %d\n" % (cnt, (time-start)))
		print sum_time / sum_i 
		f.close();





		


	def getRawData(self):
		return self.raw_data
			

for st in ["stap_result_10000_1000000", "stap_result_100000_1000000", "stap_result_400000_1000000"]:
	res = Result() 
	res.load_file(st)
	res.analyse_timingf("result")
	print "-----------"


