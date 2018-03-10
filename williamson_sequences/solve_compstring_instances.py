import time, sys, os.path
from subprocess32 import call
from mathcheck_common import sq

verbose = False
uselogs = False

if len(sys.argv) < 2:
	print "need order (and optionally a case #) of the search to run"
	quit()

n = int(sys.argv[1])
casetosolve = int(sys.argv[2]) if len(sys.argv) > 2 else -1

def runstr(n, c):
	if c == -1:
		return "%s" % n
	else:
		return "%s.%s" % (n, c)

inname = "input/compstring/%s.in"
logname = "logs/%s.log"
exhaustname = "exhaust/%s"
timingsname = "timings/%s.solvetime"

if not os.path.exists("exhaust"): call(["mkdir", "exhaust"])
if uselogs:
	if not os.path.exists("logs"): call(["mkdir", "logs"])
if not os.path.exists("timings"): call(["mkdir", "timings"])

if n%2 == 0:
	d = 2
elif n%3 == 0:
	d = 3
elif n%5 == 0:
	d = 5
else:
	print "Invalid divisor"
	quit()
l = n/d

if not os.path.exists("maplesat_static"):
	call("make maplesat_static".split(" "))

print "ORDER {0}: Solve SAT instances".format(n)

for c in range(len(sq[n])):

	if casetosolve != -1 and casetosolve != c:
		continue

	if uselogs:
		logfile = open(logname % runstr(n, c), "w")
	else:
		logfile = open("/dev/null", "w")

	call("touch {0}".format(exhaustname % runstr(n, c)).split(" "))
	call("rm {0}".format(exhaustname % runstr(n, c)).split(" "))
	call("touch {0}".format(exhaustname % runstr(n, c)).split(" "))

	if not os.path.exists("matchedseqns/{0}.{1}.{2}.inequiv".format(n, c, l)):
		continue

	f = open("matchedseqns/{0}.{1}.{2}.inequiv".format(n, c, l), "r")
	lines = f.readlines()
	f.close()

	start = time.time()
	totalsolved = 0

	for li in range(len(lines)):

		pos = lines[li][:-2].split(" ")
		pos = map(int, pos)
		assert(len(pos)==4*l)

		compstring = "{0},".format(d)
		for x in pos:
			compstring += "{0},".format(x)
		compstring = compstring[:-1]

		command = "./maplesat_static -no-pre -verb={1} -order={0} ".format(n, 1 if uselogs else 0) + inname % runstr(n, -1) + " -exhaustive=" + exhaustname % runstr(n, c)
		command += " -filtering"
		command += " -compstring=" + compstring

		if verbose:
			print command

		call(command.split(" "), stdout=logfile)

		totalsolved += 1

	print "  Case {0}: {1} SAT instances solved in %.2f seconds".format(c, totalsolved) % (time.time()-start)

	f = open(timingsname % runstr(n, c), "w")
	f.write("%.2f\n" % (time.time()-start))
	f.close()
