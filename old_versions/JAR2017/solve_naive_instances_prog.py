import time, sys, os.path, glob, math
from subprocess32 import call, TimeoutExpired
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

inname = "input/naive/%s.in"
resultname = "results/naive_prog/%s.out"
logname = "output/naive_prog/%s.log"

if not os.path.exists("output"): call(["mkdir", "output"])
if not os.path.exists("output/naive_prog"): call(["mkdir", "output/naive_prog"])
if not os.path.exists("results"): call(["mkdir", "results"])
if not os.path.exists("results/naive_prog"): call(["mkdir", "results/naive_prog"])

for n in range(n1, n2+1):
	for c in range(len(sq[n])):
		f = open("williamson_config.config", "w")
		f.write(str(n)+"\n")
		f.write(str(sq[n][c][0]*(-1 if n%2==1 and sq[n][c][0]%4!=n%4 else 1))+"\n")
		f.write(str(sq[n][c][1]*(-1 if n%2==1 and sq[n][c][1]%4!=n%4 else 1))+"\n")
		f.write(str(sq[n][c][2]*(-1 if n%2==1 and sq[n][c][2]%4!=n%4 else 1))+"\n")
		f.write(str(sq[n][c][3]*(-1 if n%2==1 and sq[n][c][3]%4!=n%4 else 1))+"\n")
		f.close()

		command = "./maplesat_static {0} {1} -programmatic-script=williamson_programmatic.py -programmatic-config=williamson_config.config".format(inname % runstr(n, -1, -1), resultname % runstr(n, c, -1))
		if sharcnet == True:
			command = "sqsub -r 24h --mpp=2G -o " + logname % runstr(n, -1, -1) + " " + command

		logfile = open(logname % runstr(n, c, -1), "w")
		print command
		if sharcnet == True:
			call(command.split(" "))
		else:
			call(command.split(" "), stdout=logfile)
		logfile.close()
