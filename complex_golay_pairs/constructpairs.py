import sys
import time
import os.path
from subprocess32 import call

numsplits = 1
verbose = False
uselogs = False

if len(sys.argv)<=2:
	print "Need order of complex Golay pairs to construct (and the case # to solve if the work has been split up)"
	quit()

n = int(sys.argv[1])
s = int(sys.argv[2]) if len(sys.argv) > 2 else 0

if not os.path.exists("pairs"): call("mkdir pairs".split(" "))
if not os.path.exists("input"): call("mkdir input".split(" "))
if uselogs:
	if not os.path.exists("logs") and uselogs: call("mkdir logs".split(" "))
if not os.path.exists("timings"): call("mkdir timings".split(" "))

if not os.path.exists("maplesat_static"):
	call("make maplesat_static".split(" "))

f = open("input/{0}.cnf".format(n), "w")
f.write("p cnf {0} 3\n{0} -{0} 0\n".format(2*n))
f.write("-1 0\n")
f.write("-2 0\n")
f.close()

if os.path.exists("pairs/pairs.{0}.{1}.txt".format(n, s)):
	call("mv pairs/pairs.{0}.{1}.txt pairs/pairs.{0}.{1}.txt.orig".format(n, s).split(" "))
call("touch pairs/pairs.{0}.{1}.txt".format(n, s).split(" "))

start = time.time()
if uselogs:
	logfile = open("logs/log.{0}.{1}.txt".format(n, s), "w")
else:
	logfile = open("/dev/null", "w")
f = open("joins/join.{0}.{1}.txt".format(n, s), "r")
count = 0
for line in f.readlines():
	count += 1
	command = "./maplesat_static -no-pre -verb={3} -order={0} -seqone={1} -exhaustive=pairs/pairs.{0}.{2}.txt input/{0}.cnf".format(n, line[:-1], s, 1 if uselogs else 0)
	if verbose:
		print command
	call(command.split(" "), stdout=logfile)
f.close()
if uselogs:
	logfile.close()
end = time.time()

if numsplits == 1:
	print "Order {0} pairing time: %.2f seconds with {1} calls to MapleSAT".format(n, count) % (end-start)
else:
	print "Order {0} split {1} pairing time: %.2f seconds with {2} calls to MapleSAT".format(n, s, count) % (end-start)

f = open("timings/{0}.{1}.pairing.time".format(n, s), "w")
f.write("%.2f\n" % (end-start))
f.close()
