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
	elif k == -1 and c == "*":
		return "%d.*" % n
	elif k == -1:
		return "%d.%d" % (n, c)
	elif k == "*" and c == "*":
		return "%d.*.*" % n
	elif k == "*":
		return "%d.%d.*" % (n, c)
	else:
		return "%d.%d.%d" % (n, c, k)

inname = "input/squaredecomp/%s.in"
resultname = "results/squaredecompprog/%s.out"
logname = "output/squaredecompprog/%s.log"

if not os.path.exists("output"): call(["mkdir", "output"])
if not os.path.exists("output/squaredecompprog"): call(["mkdir", "output/squaredecompprog"])
if not os.path.exists("results"): call(["mkdir", "results"])
if not os.path.exists("results/squaredecompprog"): call(["mkdir", "results/squaredecompprog"])

for n in range(n1, n2+1):
	command = "python generate_squaredecomp_instances.py {0}".format(n)
	call(command.split(" "))

	files = glob.glob(inname % runstr(n, "*", -1))

	for f in files:
		c = int(f.split(".")[-2])

		command = "./maplesat_static -no-pre -xnormult -cardinality -ordering -order={0} -carda={1} -cardb={2} -cardc={3} -cardd={4} ".format(n, sq[n][c][0]*(-1 if sq[n][c][0] % 4 == 3 else 1), sq[n][c][1]*(-1 if sq[n][c][1] % 4 == 3 else 1), sq[n][c][2]*(-1 if sq[n][c][2] % 4 == 3 else 1), sq[n][c][3]*(-1 if sq[n][c][3] % 4 == 3 else 1)) + inname % runstr(n, c, -1) + " " + resultname % runstr(n, c, -1)
		if sharcnet == True:
			command = "sqsub -r 24h --mpp=2G -o " + logname % runstr(n, c, -1) + " " + command

		logfile = open(logname % runstr(n, c, -1), "w")
		print command
		if sharcnet == True:
			call(command.split(" "))
		else:
			call(command.split(" "), stdout=logfile)
		logfile.close()

#call(["python", "timings.py", logname % runstr(n, "*", -1)])
