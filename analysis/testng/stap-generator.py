import os 
import sys


def get_template(path):
	f = open(path, "r")
	res = f.read()
	f.close()
	
	return res

def prepare_globals(monitor):
	res = ""
	for item in monitor:
		res += "global %s = 0;\n" % item

	return res

def prepare_prints(monitor):
	res = ""
	for item in monitor:
		res += "printf(\"%s %%d\\n\", %s);\n" % (item, item)

	return res

def prepare_conditions(monitor):
	res = ""

	for item in monitor:
		if res == "":
			res += "\t\t\tif (execname() == \"%s\") \n" % item
		else:
			res += "\t\t\t else if (execname() == \"%s\") \n" % item
		
		res += "\t\t\t\t { %s += gettimeofday_ns() - last;}\n" % item
	

	res += "\t\t\t else {overhead += gettimeofday_ns() - last;}\n"
		

	return res

monitor = []
for ar in sys.argv[1:]:
	monitor += [ar]




template = get_template(os.path.dirname(os.path.realpath(__file__)) + "/template.tpl")
template = template.replace("#GLOBALS", prepare_globals(monitor))
template = template.replace("#CONDITIONS", prepare_conditions(monitor))
template = template.replace("#PRINTS", prepare_prints(monitor))
print(template)




