import glob

def get_content(filename):
	res = []	
	f = open(filename)
	for line in f:
		line = line.strip()
		if len(line) > 0 and line[0] == "0":
			splitted = line.split(" ")
			res += [(int(splitted[0]), int(splitted[1]))]

	f.close()
	return res


contents = []


for file in glob.glob("*.res"):
	contents += [get_content(file)]

res = []
fcount = len(contents)
for i in range(len(contents[0])):
	cnt = 0;
	for f in range(fcount):
		#print(contents[f][i], end=" ")
		cnt += contents[f][i][1]
	print("%d %f" % (i, cnt / fcount))




	
		
