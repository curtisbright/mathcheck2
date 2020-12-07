# Script to generate the A2 SAT instance for a given case

import sys, os

if len(sys.argv) <= 1:
	print "Need case # of the SAT instance to generate"
	quit()

case = int(sys.argv[1])

if not case in range(1, 67):
	print "Case needs to be an integer between 1 and 66"
	quit()

# Set initial entries
f = open(os.path.join(os.path.dirname(__file__), "initial/{0}.initial".format(case)))
A = []
for line in f.readlines():
	A.append(list(line[:-1]))
f.close()

# Compute column sums in A1
colsums = [sum([int(A[i][j]) for i in range(6)]) for j in range(19)]

# Return the variable number corresponding to the (i, j)th entry of A
# where 0 <= i < 111 denotes the row and 0 <= j < 100 denotes the column (last 11 columns unused)
def var(i, j):
	return 100*(i+1)+j+1

clauses = []
max_lines = 43
max_columns = 19
total_vars = var(max_lines, max_columns)

# Generate variables for undetermined entries of A and represent known entries by 'T' or 'F'
for i in range(max_lines):
	for j in range(max_columns):
		if A[i][j] == '0':
			clauses.append("-{0} 0".format(var(i, j)))
			A[i][j] = 'F'
		elif A[i][j] == '1':
			clauses.append("{0} 0".format(var(i, j)))
			A[i][j] = 'T'
		elif A[i][j] == ' ':
			A[i][j] = var(i, j)

# Generate a clause containing the positive literals of the variables in the set X
def generate_clause(X):
	if 'T' in X or X==set([]):
		return
	clause = ""
	for x in X - {'F'}:
		clause += str(x) + " "
	clauses.append(clause + "0")

# Generate a clause containing the negative literals of the variables in the set X
def generate_negative_clause(X):
	if 'F' in X:
		return
	clause = ""
	for x in X - {'T'}:
		clause += str(-x) + " "
	clauses.append(clause + "0")

# Generate a clause specifying (x1 & ... & xn) -> (y1 | ... | yk)
# where X = {x1, ..., xn} and Y = {y1, ..., yk}
def generate_implication_clause(X, Y):
	if 'F' in X or 'T' in Y:
		return
	clause = ""
	for x in X - {'T'}:
		clause += str(-x) + " "
	for y in Y - {'F'}:
		clause += str(y) + " "
	clauses.append(clause + "0")

# Generate clauses encoding that the vector X is lexicographically greater than or equal to vector Y
def generate_lex_clauses(X, Y):
	global total_vars
	n = len(X)

	generate_implication_clause({X[0]}, {Y[0]})
	generate_implication_clause({X[0]}, {total_vars+1})
	generate_clause({Y[0], total_vars+1})
	for k in range(1, n-1):
		generate_implication_clause({X[k], total_vars+k}, {Y[k]})
		generate_implication_clause({X[k], total_vars+k}, {total_vars+k+1})
		generate_implication_clause({total_vars+k}, {Y[k], total_vars+k+1})
	generate_implication_clause({X[n-1], total_vars+n-1}, {Y[n-1]})

	total_vars += n-1

# Generate clauses encoding that exactly s variables in X are assigned true (using sequential counters)
def generate_adder_clauses(X, s):
	global total_vars
	n = len(X)
	k = s+1

	S = [[0 for j in range(k+1)] for i in range(n+1)]

	for i in range(n+1):
		S[i][0] = 'T'

	for j in range(1, k+1):
		S[0][j] = 'F'

	S[n][s] = 'T'
	S[n][k] = 'F'

	# Uses additional variables
	for i in range(n+1):
		for j in range(k+1):
			if S[i][j] == 0:
				total_vars += 1
				S[i][j] = total_vars

	for i in range(1, n+1):
		for j in range(1, k+1):
			generate_implication_clause({S[i-1][j]}, {S[i][j]})
			generate_implication_clause({X[i-1], S[i-1][j-1]}, {S[i][j]})
			generate_implication_clause({S[i][j]}, {S[i-1][j], X[i-1]})
			generate_implication_clause({S[i][j]}, {S[i-1][j], S[i-1][j-1]})

# Generate clauses that say that any two distinct lines do not intersect twice
for i in range(max_lines):
	for j in range(i+1, max_lines):
		for k in range(max_columns):
			for l in range(k+1, max_columns):
				generate_negative_clause({A[i][k], A[j][k], A[i][l], A[j][l]})

# Generate clauses that say that A2 rows are lexicographically ordered
for i in range(6, max_lines-1):
	S1 = [var(i,j) for j in range(max_columns)]
	S2 = [var(i+1,j) for j in range(max_columns)]
	generate_lex_clauses(S2, S1)

# Generate clauses that say there are 3 points on each line in A2
for i in range(6, max_lines):
	S = [var(i,j) for j in range(max_columns)]
	generate_adder_clauses(S, 3)

# Generate clauses that say there are 11 lines through each of the first 19 points
for j in range(19):
	S = [var(i,j) for i in range(6, 43)]
	generate_adder_clauses(S, 9-2*colsums[j])

# Output SAT instance in DIMACS format
print "p cnf {0} {1}".format(total_vars, len(clauses))
for clause in clauses:
	print clause

