import math, sys, os.path, glob
from subprocess32 import call

if not os.path.exists("input"):
        call(["mkdir", "input"])
if not os.path.exists("input/naive"):
	call(["mkdir", "input/naive"])

if not os.path.exists("output"):
        call(["mkdir", "output"])
if not os.path.exists("output/naive"):
	call(["mkdir", "output/naive"])

if not os.path.exists("results"):
        call(["mkdir", "results"])
if not os.path.exists("results/naive"):
	call(["mkdir", "results/naive"])

if len(sys.argv) < 2:
	print "Need order of instance to generate"
	quit()

n = int(sys.argv[1])

f = open("input/naive/%d.in" % n, "w")
#dependency on this file; inital set of constraints calculated.
call(["python", "hadamard_williamson_circ_SAT_binary_adder_squares_all.py", str(n)], stdout=f)
f.close()
f = open("input/naive/%d.in" % n, "r")
origlines = f.readlines()
f.close()
origvars = int(origlines[0].split(" ")[-2])
orignumclauses = int(origlines[0].split(" ")[-1])

indices = [0*(n/2+1)+1, 1*(n/2+1)+1, 2*(n/2+1)+1, 3*(n/2+1)+1]
clauses = []
# Add clauses based on the identity a[0]*b[0]*c[0]*d[0] = -a[i]*b[i]*c[i]*d[i] for odd n
if n % 2 == 1:
	for j in range(1,n/2+1):
		clauses.append("%d %d %d %d 0" % (-(indices[0]+j), -(indices[1]+j), -(indices[2]+j), -(indices[3]+j)))
		clauses.append("%d %d %d %d 0" % (-(indices[0]+j), -(indices[1]+j), (indices[2]+j), (indices[3]+j)))
		clauses.append("%d %d %d %d 0" % (-(indices[0]+j), (indices[1]+j), -(indices[2]+j), (indices[3]+j)))
		clauses.append("%d %d %d %d 0" % (-(indices[0]+j), (indices[1]+j), (indices[2]+j), -(indices[3]+j)))
		clauses.append("%d %d %d %d 0" % ((indices[0]+j), -(indices[1]+j), -(indices[2]+j), (indices[3]+j)))
		clauses.append("%d %d %d %d 0" % ((indices[0]+j), -(indices[1]+j), (indices[2]+j), -(indices[3]+j)))
		clauses.append("%d %d %d %d 0" % ((indices[0]+j), (indices[1]+j), -(indices[2]+j), -(indices[3]+j)))
		clauses.append("%d %d %d %d 0" % ((indices[0]+j), (indices[1]+j), (indices[2]+j), (indices[3]+j)))

f = open("input/naive/%d.in" % n, "w")
f.write("p cnf %d %d\n" % (origvars, orignumclauses+len(clauses)))
for line in origlines[1:]:
	f.write(line)
for cl in clauses:
	f.write(cl+"\n")
f.close()
