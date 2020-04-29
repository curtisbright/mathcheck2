# Generate block symmetry breaking clauses in cnf format

import sys

if len(sys.argv) <= 1:
	print "Need case to generate symmetry breaking clauses for (1a, 1b, 1c)"
	quit()

case = sys.argv[1]

if case=="1b" or case=="1c":
	cols = 24
else:
	cols = 23

f = open("exhaust/{0}.{1}.exhaust-icnf.sorted".format(case, cols), "r")	# Clauses blocking cases where first block is not of minimal index (icnf format)
g = open("exhaust/{0}.{1}.exhaust-cnf.sorted".format(case, cols), "w")	# Clauses blocking cases where first block is not of minimal index (cnf format)

curvar = 8880

for line in f.readlines():
	if "a" in line:
		splitline = line.split(" ")[1:-1]
		splitline = map(int, splitline)
		splitline = map(lambda x: -x, splitline)
		splitline.append(curvar)
		splitline.append(0)
		splitline = map(str, splitline)
		g.write("-{0} {1} 0\n".format(curvar, curvar-1))
		#for i in range(curvar,8880,-1):
		#	g.write("-{0} {1} 0\n".format(curvar, i-1))
		g.write(" ".join(splitline)+"\n")
		curvar += 1
	else:
		g.write(str(-curvar)+" "+line)

f.close()
g.close()
