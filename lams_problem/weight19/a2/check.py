# Check that all rejected completions are isomorphic to a recorded solution
# Uses labelings provided by Traces but these are explicitly verified and not assumed to be trustworthy

# The label files consist of the labellings provided by Traces in order to translate the incidence graph of A2 into a canonical form
# where the first 19 vertices of the incidence graph represent the columns of A2 and the remaining 43 vertices represent the rows of A2

import sys
import time
start = time.clock()

if len(sys.argv) <= 1:
	print "Need case to check"
	quit()

def readmatrix(line):
	M = [[0 for j in range(19)] for i in range(43)]
	vs = map(abs, map(int, line.split(" ")))
	for v in vs:
		if v > 0:
			vi = ((v-1) / 100)-1
			vj = (v-1) % 100
			M[vi][vj] = 1
	return M

def performrowswaps(M, labs):
	N = [[0 for j in range(19)] for i in range(43)]
	for i in range(43):
		N[i] = M[labs[i]]
	return N
	
def performcolswaps(M, labs):
	N = [[0 for j in range(19)] for i in range(43)]
	for i in range(43):
		for j in range(19):
			N[i][j] = M[i][labs[j+43]-43]
	return N
	
def performswaps(M, labs):
	return performcolswaps(performrowswaps(M, labs), labs)

def to_tuple(M):
	return tuple([tuple([M[i][j] for j in range(19)]) for i in range(43)])

case = int(sys.argv[1])

if not case in range(1, 67):
	print "Case needs to be an integer between 1 and 66"
	quit()

matrices = set()
records = []
labels = []

# Open file containing recorded completions
with open("out/a2.{0}.recorded".format(case), "r") as f:
	records += f.readlines()
# Open file containing the labels required to translate each recorded completion into canonical form
with open("out/a2.{0}.recorded.lab".format(case), "r") as f:
	labels += f.readlines()

# Translate each recorded completion into canonical form
for i in range(len(records)):
	record = records[i]
	label = labels[i]

	label = map(int, label.split(" ")[:-1])
	m = readmatrix(record[2:-3])
	m = performswaps(m, label)
	
	matrices.add(to_tuple(m))

# Open file containing rejected completions
with open("out/a2.{0}.rejected".format(case), "r") as f:
	rejects = f.readlines()
# Open file containing the labels required to translate each rejected completion into canonical form
with open("out/a2.{0}.rejected.lab".format(case), "r") as f:
	labels = f.readlines()

# Translate each rejected completion into canonical form and ensure that it is isomorphic to some recorded completion
for i in range(len(rejects)):
	reject = rejects[i]
	label = labels[i]

	label = map(int, label.split(" ")[:-1])
	M = readmatrix(reject[2:-3])
	M = performswaps(M, label)
	
	assert(to_tuple(M) in matrices)

print "All {0} rejected completions verified to be isomorphic to one of {1} recorded completions in %.2f sec".format(len(rejects), len(matrices)) % (time.clock()-start)
