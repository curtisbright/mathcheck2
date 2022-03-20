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

inname = "input/comp/%s.in"
compname = "input/comp/%s.comp"
assumname = "input/comp/%s.assum"
#prodvarname = "input/prodvar/%d.prodvars"
resultname = "results/compprog/%s.out"
logname = "output/compprog/%s.log"

if not os.path.exists("output"): call(["mkdir", "output"])
if not os.path.exists("output/compprog"): call(["mkdir", "output/compprog"])
if not os.path.exists("results"): call(["mkdir", "results"])
if not os.path.exists("results/compprog"): call(["mkdir", "results/compprog"])

for n in range(n1, n2+1):
    # Generate SAT instance
    #command = "python2 generate_compression_instances.py {0}".format(n)
    #call(command.split(" "))

    files = glob.glob(compname % runstr(n, "*", "*"))
    count = 0
    tottime = 0

    for f in files:
        k = int(f.split(".")[-2])
        c = int(f.split(".")[-3])

        count += 1
        command = "./maplesat_static {0} {1} -no-pre -xnormult -order={2} -carda={3} -cardb={4} -cardc={5} -cardd={6} -compsums={7}".format(inname % runstr(n,c,-1), resultname % runstr(n, c, k), n, sq[n][c][0]*(-1 if sq[n][c][0] % 4 == 3 else 1), sq[n][c][1]*(-1 if sq[n][c][1] % 4 == 3 else 1), sq[n][c][2]*(-1 if sq[n][c][2] % 4 == 3 else 1), sq[n][c][3]*(-1 if sq[n][c][3] % 4 == 3 else 1), compname % runstr(n, c, k))
        if sharcnet == True:
            command = "sqsub -r 5m --mpp=2G -o " + logname % runstr(n, c, k) + " " + command

        logfile = open(logname % runstr(n, c, k), "w")
        print command
        if sharcnet == True:
            call(command.split(" "))
        else:
            call(command.split(" "), stdout=logfile)
        logfile.close()

        #logfile = open(logname % runstr(n, c, k), "r")
        #for line in logfile.readlines():
        #    if "CPU time" in line:
        #        time = float(line.split(" ")[-2])
        #        tottime += time
        #logfile.close()

        call("python2 read_results.py {0} {1}".format(resultname % runstr(n, c, k), n).split(" "))
        #resfile = open(resultname % runstr(n, c, k), "r")
        #reslines = resfile.readlines()
        #print "%s time: %0.2f" % (reslines[0][:-1], time)
        #resfile.close()

    #print "solved %d instances in %0.2fs" % (count, tottime)
