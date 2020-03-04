from PIL import Image, ImageDraw
import sys



class Draw:
	def __init__(self, results):
		self.results = results;		
		pass;
	


	def minRange(self):
		return self.results.raw_data[0][2];		

		
	def maxRange(self):
		return self.results.raw_data[-1][2];

	def draw(self, filename):
		min = self.minRange()
		max = self.maxRange()
		range = max - min
		
		datalen = len(self.results.raw_data)
		
		#previous = min
		#for line in self.results.raw_data:
		#print line[2] - previous
		#previous = line[2] 


		#print min, max, range
		im = Image.new('RGB', (datalen, 30), color = 'red')

		i = 0		
		for r in self.results.raw_data:
			i += 1



		draw = ImageDraw.Draw(im)
		draw.line((0, 0) + im.size, fill=128)
		draw.line((0, im.size[1], im.size[0], 0), fill=128)
		del draw

		im.save(filename, "PNG")
		





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
	
	def analyse_timing(self):
		tmp = {}		
		for r in self.raw_data:
			#print r[1]
			tmp[r[1]] = 0
		i = 0
		start = 0
		cnt = 0
		for r in self.raw_data:
			id = r[1]
			state = r[0]
			time = long(r[2])
			name = r[3]
				
			if state == "ON":
				start = time	
			elif state=="OFF" and i != 0:
				#print(self.proc_info[id], tmp[id], time, start, time-start)
				tmp[id] += (time-start)
				if name == "rt_sample":
					cnt += 1		
					#print cnt, (time-start) 
			i += 1
		return tmp 


	def analyse_timingf(self, proc1, proc2, filename):
		start = 0
		cnt = 0
		i = 0

		f = open(filename, "w")
		for r in self.raw_data:
			id = r[1]
			state = r[0]
			time = long(r[2])
			name = r[3]
				
			if state == "ON":
				start = time
				i += 1
			elif state=="OFF" and i != 0:
				if name == proc1 or name == proc2 :
					cnt += 1		
					if name == proc1:					
						f.write("%d %d\n" % (cnt, (time-start)))
		f.close();




	def sum_NR(self, processes):
		sum = 0
		
		for key in processes:
			if self.proc_info[key] != "rt_sample" or self.proc_info[key] == "rt_sample1":
				sum += processes[key]
		return sum


		

	def print_analyse_timing(self):
		tmp = self.analyse_timing();
		for key in tmp:
			print key, tmp[key], self.proc_info[key]
			#, self.proc_info[key], tmp[key]


	def print_analyse_timing_gnuplot(self):
		i = 1;		
		tmp = self.analyse_timing();
		for key in tmp:
			print i, self.proc_info[key], tmp[key]
			i += 1

	def print_analyse_timing_gnuplot_sum(self, filename):
		i = 0		
		tmp = self.analyse_timing();
		f = open(filename, "w")
		for key in tmp:

			if self.proc_info[key] == "rt_sample" or self.proc_info[key] == "rt_sample1":			
				f.write("%d %s %d\n" % (i, self.proc_info[key], tmp[key]))
				print i, self.proc_info[key], tmp[key]
				i += 1
		f.write("%d non-RT %d\n" % (i, self.sum_NR(tmp)))
		f.close()


		

	def print_verbose(self):
		for data in self.raw_data:
			print data
		

		
	def draw(self):
		print("drawing")

	def getRawData(self):
		return self.raw_data
			

res = Result() 
res.load_file("../../systemtap/stap_result")

res.print_analyse_timing_gnuplot_sum("points_sum.dat")
res.analyse_timingf("rt_sample", "rt_sample1", "points_runtime.dat")
res.analyse_timingf("rt_sample1", "rt_sample", "points_runtime1.dat")


