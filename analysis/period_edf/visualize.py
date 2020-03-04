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

		f = open(filename, "w")
		for r in self.raw_data:
			id = r[1]
			state = r[0]
			time = long(r[2])
			name = r[3]
				
			if state == "ON":
				if name == "deadline":				
					if start != -1:
						f.write("%d %d\n" % (cnt, (time-start)))
						print (time-start), ",", 
						cnt += 1						
					
					start = time

							#elif state=="OFF" and i != 0:
			#	if name == "rt_sample" :
			#		cnt += 1		
			#		f.write("%d %d\n" % (cnt, (time-start)))
		f.close();





		


	def getRawData(self):
		return self.raw_data
			

res = Result() 
res.load_file("../../systemtap/stap_result")

res.analyse_timingf("points_period.dat")


