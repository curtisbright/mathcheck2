# Generate block symmetry breaking clauses in icnf format

import sys

if len(sys.argv) <= 1:
	print "Need case to generate symmetry breaking clauses for (1a, 1b, 1c)"
	quit()

remove_blocks = True

case = sys.argv[1]

colswap = [None for i in range(8)]
rowswap = [None for i in range(8)]

execfile("swaps/swaps_{0}.py".format(sys.argv[1]))

if case=="1b" or case=="1c":
	cols = 24
else:
	cols = 23

f = open("exhaust/{0}.{1}.exhaust-blocking.sorted".format(case, cols), "r")	# Possibilities for first block including blocking of other isomorphic possibilities
g = open("exhaust/{0}.{1}.exhaust-icnf.sorted".format(case, cols), "w")	# Clauses blocking cases where first block is not of minimal index (icnf format)

def to_vars(matrix):
	result = []

	for i in range(66):
		for j in range(80):
			if matrix[i][j] == "1":
				varno = 111*j+i+1
				result.append(-varno)

	result = sorted(result, reverse=True)
	result.append(0)

	result = map(str, result)
	return " ".join(result)+"\n"

def getcols(case, r):
	with open("initial/initial_matrix_{0}".format(case)) as f:
		initial_P = f.read()
	P = []
	for row in initial_P.split('\n')[0:8]:
		P.append(list(row))

	identical_cols = []
	for i in range(1, len(P[0])):
		if P[r][i] == '1' and [k for k in range(8) if P[k][i] == '1'] == [k for k in range(8) if P[k][i-1] == '1']:
			identical_cols.append(i)

	return identical_cols

start = [getcols(case, c)[0]-1 for c in range(8)]
end = [getcols(case, c)[-1]+1 for c in range(8)]

def printmatrix(matrix):
	for i in range(66):
		line = "".join(matrix[i])
		if line != "0"*80:
			print i, line
	print ""

for line in f.readlines():
	if "a" in line:
		g.write(line)
		continue

	matrix = [[list("0"*80) for i in range(66)] for c in range(8)]

	assums = line.split(" ")[:-1]
	for assum in assums:
		row = (abs(int(assum))-1)/111
		col = (abs(int(assum))-1)%111

		for c in range(8):
			if colswap[c] != None:
				matrix[c][colswap[c][col]][rowswap[c][row]] = "1"

	for c in range(8):
		if colswap[c] != None:
			matrix[c][start[c]:end[c]] = sorted(matrix[c][start[c]:end[c]], reverse=True)
			g.write(to_vars(matrix[c]))

f.close()
g.close()
