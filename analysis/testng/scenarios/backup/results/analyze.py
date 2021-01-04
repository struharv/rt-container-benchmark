def get_file(filename):
	f = open(filename, "r")
	res = f.read()
	f.close()
	
	return res



def getValue(key, lines):
	for l in lines:
		buf = l.split(" ")
		if buf[0] == key:
			if len(buf[1:]) > 1:
				return buf[1:]
			else:
				return buf[1]

def getMultiple(key, lines):
	res = []

	for l in lines:
		buf = l.split(" ")
		if buf[0].startswith(key):
			res += [buf]

	
	return res

def _duration(lines):
	return int(getValue("End", lines))-int(getValue("Start", lines))

def _sum(key, lines):
	lst = getMultiple(key, lines)
	sum = 0	
	for l in lst:
		print l, sum
		sum += int(l[1])
	return sum

def analyze(filename):
	txt = get_file(filename)	
	lines = txt.split("\n")
		
	#print lines

	duration=_duration(lines)
	nrt = _sum("nr", lines)	
	rt = _sum("r", lines)
	
	res = {}
	res["duration"] = duration
	res["nrt"] = nrt
	res["rt"] = rt
	res["overhead"]=getValue("Overhead", lines)
	res["preemptions"]=getValue("Preemptions", lines)
	
	return res

def graph():
	data = []	
	data += [analyze("scenario1/scenario1_nr10_0.txt")]
	data += [analyze("scenario1/scenario1_nr20_0.txt")]
	data += [analyze("scenario1/scenario1_nr30_0.txt")]
	data += [analyze("scenario1/scenario1_nr50_0.txt")]

	res = []
	for d in data:
		res += [[d["nrt"], d["rt"], d["overhead"], d["preemptions"]]]

		print res

	f = open("scenario1/graph1/data.dat", "w")
	i = 0
	for r in res:
		f.write(str(i)+" ")
		for d in r:
			f.write("%s " % str(d))
		f.write("\n")

		i += 1
	f.close()
		

graph()

