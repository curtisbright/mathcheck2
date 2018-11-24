import time, sys, os.path, glob, math
from subprocess32 import call
from mathcheck_common import sq

sharcnet = False

if len(sys.argv) < 2:
	print "need order (or min and max orders) of search to run"
	quit()

n1 = int(sys.argv[1])
if len(sys.argv) > 2:
	n2 = int(sys.argv[2])
else:
	n2 = n1

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
resultname = "results/compunsatcoreprog/%s.out"
logname = "output/compunsatcoreprog/%s.log"
assumname = "input/comp/%s.assum"
prodvarname = "input/naive/%d.prodvars"

if not os.path.exists("output"): call(["mkdir", "output"])
if not os.path.exists("output/compunsatcoreprog"): call(["mkdir", "output/compunsatcoreprog"])
if not os.path.exists("results"): call(["mkdir", "results"])
if not os.path.exists("results/compunsatcoreprog"): call(["mkdir", "results/compunsatcoreprog"])

for n in range(n1, n2+1):
	files = glob.glob(assumname % runstr(n, "*", "*"))
	tottime = 0
	count = 0
	skipped = 0
	alreadysolved = 0
	unsatcores = []

	def skip_instance(list_assumptions, unsatcores):
		set_assumptions = set(list_assumptions)
		for core in unsatcores:
			if set(core).issubset(set_assumptions):
				return True
		return False

	def update_unsatcores(reslines, unsatcores):
		unsatcore = []
		for line in reslines[1:]:
			unsatcore.append(int(line))
		if len(unsatcore) < 25:
			unsatcores.append(unsatcore)

	for f in files:
		k = int(f.split(".")[-2])
		c = int(f.split(".")[-3])

		if os.path.exists(resultname % runstr(n, c, k)):
			resfile = open(resultname % runstr(n, c, k), "r")
			reslines = resfile.readlines()
			if len(reslines) > 0 and "UNSAT" in reslines[0]:
				update_unsatcores(reslines, unsatcores)
			resfile.close()
			if len(reslines) > 0 and "SAT" in reslines[0]:
				alreadysolved += 1
				continue

		assumfile = open(assumname % runstr(n, c, k))
		assumlines = assumfile.readlines()
		assumfile.close()
		assumptions = []
		for line in assumlines:
			assumptions.append(int(line))

		if skip_instance(assumptions, unsatcores):
			skipped += 1
			print "Instance %s skipped" % f
			continue

		count += 1
		command = "./maplesat_static -no-pre -cardinality -xnormult -order={0} -carda={1} -cardb={2} -cardc={3} -cardd={4} -assumptions=".format(n, sq[n][c][0]*(-1 if sq[n][c][0] % 4 == 3 else 1), sq[n][c][1]*(-1 if sq[n][c][1] % 4 == 3 else 1), sq[n][c][2]*(-1 if sq[n][c][2] % 4 == 3 else 1), sq[n][c][3]*(-1 if sq[n][c][3] % 4 == 3 else 1)) + assumname % runstr(n, c, k) + " " + inname % runstr(n, c, -1) + " " + resultname % runstr(n, c, k)
		#command = "./maplesat_static -no-pre -cardinality -xnormult -order={0} -carda={1} -cardb={2} -cardc={3} -cardd={4} -prodvars={5} -assumptions=".format(n, sq[n][c][0]*(-1 if sq[n][c][0] % 4 == 3 else 1), sq[n][c][1]*(-1 if sq[n][c][1] % 4 == 3 else 1), sq[n][c][2]*(-1 if sq[n][c][2] % 4 == 3 else 1), sq[n][c][3]*(-1 if sq[n][c][3] % 4 == 3 else 1), prodvarname % n) + assumname % runstr(n, c, k) + " " + inname % runstr(n, c, -1) + " " + resultname % runstr(n, c, k)
		if sharcnet == True:
			command = "sqsub -r 5m --mpp=2G -o " + logname % runstr(n, c, k) + " " + command

		logfile = open(logname % runstr(n, c, k), "w")
		print command
		if sharcnet == True:
			call(command.split(" "))
		else:
			call(command.split(" "), stdout=logfile)
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
		if "UNSAT" in reslines[0]:
			update_unsatcores(reslines, unsatcores)
		resfile.close()

	print "solved %d instances in %0.2fs, %d instances already solved, %d instances eliminated by using unsat cores" % (count, tottime, alreadysolved, skipped)
