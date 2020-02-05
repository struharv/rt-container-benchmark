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


		print min, max, range
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

		start = 0
		for r in self.raw_data:
			id = r[1]
			state = r[0]
			time = long(r[2])
				
			if state == "ON":
				start = time	
			else:
				#print(self.proc_info[id], tmp[id], time, start, time-start)
				tmp[id] += (time-start)
				
		return tmp


	def print_analyse_timing(self):
		tmp = self.analyse_timing();
		for key in tmp:
			print key, tmp[key], self.proc_info[key]
			#, self.proc_info[key], tmp[key]
		
	def draw(self):
		print("drawing")

	def getRawData(self):
		return self.raw_data
			
		
	




res = Result() 
res.load_file("tee")
#res.analyse_timing()
res.print_analyse_timing()


draw = Draw(res)
draw.draw("/tmp/somethingx.png")

