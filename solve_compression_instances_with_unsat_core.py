import time, sys, os.path, glob, math
from subprocess32 import call, TimeoutExpired

sharcnet = False

if len(sys.argv) < 2:
	print "need order of search to run"
	quit()

n = int(sys.argv[1])

def runstr(n, c, k):
	if k == -1 and c == -1:
		return "%s" % n
	elif k == -1:
		return "%d.%d" % (n, c)
	elif k == "*" and c == "*":
		return "%d.*.*" % n
	elif k == "*":
		return "%d.%d.*" % (n, c)
	else:
		return "%d.%d.%d" % (n, c, k)

inname = "input/comp/%s.in"
resultname = "results/comp/%s.out"
logname = "output/comp/%s.log"
assumname = "input/comp/%s.assum"

files = glob.glob(assumname % runstr(n, "*", "*"))
tottime = 0
count = 0
unsatcores = []

def skip_instance(list_assumptions, unsatcores):
	set_assumptions = set(list_assumptions)
	for core in unsatcores:
		if set(core).issubset(set_assumptions):
			return True
	return False

for f in files:
	k = int(f.split(".")[-2])
	c = int(f.split(".")[-3])

	assumfile = open(assumname % runstr(n, c, k))
	assumlines = assumfile.readlines()
	assumfile.close()
	assumptions = []
	for line in assumlines:
		assumptions.append(int(line))

	if skip_instance(assumptions, unsatcores):
		continue

	count += 1
	command = "./maplesat_static -no-pre -assumptions=" + assumname % runstr(n, c, k) + " " + inname % runstr(n, -1, -1) + " " + resultname % runstr(n, c, k)
	callcommand = ["./maplesat_static", "-no-pre", "-assumptions=" + assumname % runstr(n, c, k), inname % runstr(n, -1, -1), resultname % runstr(n, c, k)]
	if sharcnet == True:
		command = "sqsub -r 5m --mpp=2G -o " + logname % runstr(n, c, k) + " " + command
		callcommand = ["sqsub", "-r", "5m", "--mpp=2G", "-o", logname % runstr(n, c, k)] + callcommand

	logfile = open(logname % runstr(n, c, k), "w")
	print command
	if sharcnet == True:
		call(callcommand)
	else:
		call(callcommand, stdout=logfile)
	logfile.close()

	logfile = open(logname % runstr(n, c, k), "r")
	for line in logfile.readlines():
		if "CPU time" in line:
			time = float(line.split(" ")[-2])
			tottime += time
	logfile.close()

	resfile = open(resultname % runstr(n, c, k), "r")
	reslines = resfile.readlines()
	print "%s time: %0.2f" % (reslines[0][:-1], time)
	if reslines[0][:-1] == "UNSAT":
		unsatcore = []
		for line in reslines[1:]:
			unsatcore.append(int(line))
		if len(unsatcore) < 25:
			unsatcores.append(unsatcore)
	resfile.close()

print "solved %d instances in %0.2fs" % (count, tottime)
