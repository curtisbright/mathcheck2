# Check that all rejected solutions are isomorphic to a recorded solution
# Uses labelings provided by Traces but these are explicitly verified and not assumed to be trustworthy

# The label files consist of the labellings provided by Traces in order to translate the incidence graph of A1 into a canonical form
# where the first 19 vertices of the incidence graph represent the columns of A1 and the remaining 6 vertices represent the rows of A1

import time
start = time.clock()

def performrowswaps(M, labs):
	N = [[0 for j in range(19)] for i in range(6)]
	for i in range(6):
		N[i] = M[labs[i]]
	return N
	
def performcolswaps(M, labs):
	N = [[0 for j in range(19)] for i in range(6)]
	for i in range(6):
		for j in range(19):
			N[i][j] = M[i][labs[j+6]-6]
	return N
	
def performswaps(M, labs):
	return performcolswaps(performrowswaps(M, labs), labs)

def to_tuple(M):
	return tuple([tuple([M[i][j] for j in range(19)]) for i in range(6)])

# Open file containing the labels required to translate each recorded A1 into canonical form
f = open("a1.recorded.lab", "r")
lines = f.readlines()
f.close

labs = []
for line in lines:
	lab = map(int, line.split(" ")[:-1])
	labs.append(lab)
matrices = set()

# Open file containing recorded A1s
g = open("a1.recorded", "r")
lines = g.readlines()
g.close()

case = 0

# Translate each recorded A1 into canonical form
for line in lines:
	M = [[0 for j in range(19)] for i in range(6)]

	var_list = map(int, line[2:-3].split(" "))
	for var in var_list:
		vi = (var/100)-1
		vj = (var%100)-1
		M[vi][vj] = 1

	matrices.add(to_tuple(performswaps(M, labs[case])))

	case += 1

# Open file containing rejected A1s
f = open("a1.rejected", "r")
lines = f.readlines()
f.close()

# Open file containing the labels required to translate each rejected A1 into canonical form
g = open("a1.rejected.lab", "r")
labs = g.readlines()
g.close()

# Translate each rejected A1 into canonical form and ensure that it is isomorphic to some recorded A1
for i in range(len(lines)):
	line = lines[i]
	lab = labs[i]

	lab = map(int, lab.split(" ")[:-1])
	
	M = [[0 for j in range(19)] for i in range(6)]
	var_list = map(int, line[2:-3].split(" "))
	for var in var_list:
		vi = (var/100)-1
		vj = (var%100)-1
		M[vi][vj] = 1
	M = performswaps(M, lab)
	
	assert(to_tuple(M) in matrices)

print "All {0} rejected solutions verified to be isomorphic to one of {1} recorded solutions in {2} sec".format(len(lines), len(matrices), time.clock()-start)
