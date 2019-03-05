import sys, os.path
from subprocess32 import call

if len(sys.argv) < 2:
	print "need order of cases to generate"
	quit()

n = int(sys.argv[1])

inname = "input/compstring/%d.in"

if not os.path.exists("input"): call(["mkdir", "input"])
if not os.path.exists("input/compstring"): call(["mkdir", "input/compstring"])

def minindex(i):
	if 2*i <= n:
		return i
	else:
		return n-i

cl = []

# Encode X[0] * X[1] * ... * X[n-1] = c where entries are in {1, -1}, i.e.,
#        X[0] + X[1] + ... + X[n-1] = c in F_2 where 1s represent 0
# The encoding uses 2^(n-1) clauses but no extra variables
def xor_clauses_1(X, c):
	n = len(X)
	Y = [-1 for i in range(n)]
	num_ones = 0
	k = n-1
	while(k >= 0):
		if (num_ones%2 == 0 and c == -1) or (num_ones%2 == 1 and c == 1):
			s = ""
			for i in range(n):
				s += "{0} ".format(X[i]*Y[i])
			s += "0"
			cl.append(s)

		k = n-1
		while(k >= 0):
			Y[k] *= -1
			if Y[k] == 1:
				num_ones += 1
				break
			num_ones -= 1
			k -= 1

numvars = 4*(n/2)+4

# Alternative encoding of xor_clauses from above
# The encoding uses 4*(n-1) clauses and n-1 new variables
def xor_clauses_2(X, c):
	global numvars
	n = len(X)
	numvars += 1
	cl.append("{0} {1} {2} 0".format(-X[0], -X[1], numvars))
	cl.append("{0} {1} {2} 0".format(X[0], -X[1], -numvars))
	cl.append("{0} {1} {2} 0".format(-X[0], X[1], -numvars))
	cl.append("{0} {1} {2} 0".format(X[0], X[1], numvars))
	for i in range(2, n):
		numvars += 1
		cl.append("{0} {1} {2} 0".format(-X[i], -(numvars-1), numvars))
		cl.append("{0} {1} {2} 0".format(X[i], -(numvars-1), -numvars))
		cl.append("{0} {1} {2} 0".format(-X[i], (numvars-1), -numvars))
		cl.append("{0} {1} {2} 0".format(X[i], (numvars-1), numvars))
	if c == 1:
		cl.append("{0} 0".format(numvars))
	else:
		cl.append("{0} 0".format(-numvars))

def xor_clauses(X, c):
	if len(X) <= 5:
		xor_clauses_1(X, c)
	else:
		xor_clauses_2(X, c)

indices = [0*(n/2+1)+1, 1*(n/2+1)+1, 2*(n/2+1)+1, 3*(n/2+1)+1]

if n%2 == 1:
	for j in range(1,n/2+1):
		if 4*j < n:
			xor_clauses([indices[0]+minindex(2*j), indices[0]+j, indices[1]+minindex(2*j), indices[1]+j, indices[2]+j, indices[2]+minindex(2*j), indices[3]+j], -1)
		elif n%3 == 0 and j == n/3:
			xor_clauses([indices[3]+j], 1)
		else:
			xor_clauses([indices[0]+minindex(2*j), indices[0]+j, indices[1]+minindex(2*j), indices[1]+j, indices[2]+j, indices[2]+minindex(2*j), indices[3]+j], 1)
else:
	cl.append("{0} -{0} 0".format(4*(n/2)+4))

# Enforce that first entries are positive
cl.append("{0} 0".format(indices[0]))
cl.append("{0} 0".format(indices[1]))
cl.append("{0} 0".format(indices[2]))
cl.append("{0} 0".format(indices[3]))

f = open(inname % n, "w")
f.write("p cnf {0} {1}\n".format(numvars, len(cl)))
for c in cl:
	f.write("{0}\n".format(c))
f.close()
