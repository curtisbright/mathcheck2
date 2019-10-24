# Weight 15 Case
# Initial assignment to the values of P where blanks signify undetermined entries
with open("initial_matrix") as f:
	initial_P = f.read()

import sys

# Total number of lines to use
max_lines = 51 if len(sys.argv) <= 1 else int(sys.argv[1])
max_columns = 75 if len(sys.argv) <= 2 else int(sys.argv[2])

# Detect if lines i and j intersect
def lines_intersect(i, j):
	for k in range(max_columns):
		if P[i][k] == 'T' and P[j][k] == 'T':
			return True
	return False

# Detect if points i and j both share a line
def points_intersect(i, j):
	for k in range(max_lines):
		if P[k][i] == 'T' and P[k][j] == 'T':
			return True
	return False

# List containing the clauses of the SAT instance
clauses = []

# Return the variable number corresponding to the (i, j)th entry of P where 0 <= i,j < 111
def var(i, j):
	return 111*i+j+1

# Generate a clause containing the positive literals of the variables in the set X
def generate_clause(X):
	if 'T' in X:
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

# Convert initial assignment from a string to a matrix
P = []
for row in initial_P.split('\n'):
	P.append(list(row))

# Generate variables for undetermined entries of P and represent known entries by 'T' or 'F'
for i in range(51):
	for j in range(111):
		if P[i][j] == '0':
			P[i][j] = 'F'
			if i in range(max_lines) and j in range(max_columns):
				clauses.append("-{0} 0".format(var(i, j)))
		elif P[i][j] == '1':
			P[i][j] = 'T'
			if i in range(max_lines) and j in range(max_columns):
				clauses.append("{0} 0".format(var(i, j)))
		elif P[i][j] == ' ':
			P[i][j] = var(i, j)

# Generate clauses that say that any two distinct lines do not intersect twice
for i in range(max_lines):
	for j in range(max(21, i+1), max_lines):
		for k in range(max_columns):
			for l in range(max(15, k+1), max_columns):
				generate_negative_clause({P[i][k], P[j][k], P[i][l], P[j][l]})

# Generate clauses that say that every light line intersects with every heavy and medium line
for i in range(21):
	for j in range(21, max_lines):
		# Ignore the case when line i and j already intersect
		if lines_intersect(i, j):
			continue

		# Find set of possible intersections
		S = {P[j][k] for k in range(max_columns) if P[i][k] == 'T' and type(P[j][k]) == int}

		# Ignore the case when line i has intersections after the maximum column in the SAT instance
		if len([P[i][k] for k in range(max_columns) if P[i][k] == 'T']) != 11:
			continue

		generate_clause(S)

# Generate clauses that say that first 15 columns intersect with B and C columns
for j in range(15):
	for i in range(15, max_columns):
		# Ignore the case when columns i and j already intersect
		if points_intersect(i, j):
			continue

		# Find set of possible intersections
		S = {P[k][i] for k in range(max_lines) if P[k][j] == 'T' and type(P[k][i]) == int}

		# Ignore the case when column j has intersections after the maximum line in the SAT instance
		if len([P[k][j] for k in range(max_lines) if P[k][j] == 'T']) != 11:
			continue

		generate_clause(S)

# Output SAT instance in DIMACS format
print "p cnf {0} {1}".format(111*(max_lines-1)+max_columns, len(clauses))
for clause in clauses:
	print clause

