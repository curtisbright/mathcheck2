# Oval Case (Weight 12)
# Initial assignment to the values of P where blanks signify undetermined entries
with open("initial_matrix") as f:
	initial_P = f.read()

# Convert initial assignment from a string to a matrix
P = []
for row in initial_P.split('\n'):
	P.append(list(row))

import sys

# The columns used in each block
blocks = [range(12+9*k, 12+9*(k+1)) for k in range(0, 11)]

# Use blocks 1 to 5 (zero-based numbering) by default
min_block = 1 if len(sys.argv) <= 1 else int(sys.argv[1])
max_block = 5 if len(sys.argv) <= 2 else int(sys.argv[2])

max_columns = 111
max_lines = 66

# Determine the columns to use in the instance
usecols = range(12)
for k in range(min_block, max_block+1):
	usecols = usecols + blocks[k]

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

# Generate variables for undetermined entries of P and represent known entries by 'T' or 'F'
for i in range(max_lines):
	for j in range(max_columns):
		if P[i][j] == '0':
			P[i][j] = 'F'
			clauses.append("-{0} 0".format(var(i, j)))
		elif P[i][j] == '1':
			P[i][j] = 'T'
			clauses.append("{0} 0".format(var(i, j)))
		elif P[i][j] == ' ':
			P[i][j] = var(i, j)

# Generate clauses that say that any two distinct lines do not intersect twice
for i in range(max_lines):
	for j in range(i+1, max_lines):
		for k in usecols:
			for l in usecols:
				if l > k:
					generate_negative_clause({P[i][k], P[j][k], P[i][l], P[j][l]})

# Generate clauses that say that first 12 columns intersect with remaining columns
for j in range(12):
	for i in usecols:
		if i > j:
			# Ignore the case when columns i and j already intersect
			if points_intersect(i, j):
				continue

			# Find set of possible intersections
			S = {P[k][i] for k in range(max_lines) if P[k][j] == 'T' and type(P[k][i]) == int}

			# Ignore the case when column j has intersections after the maximum line in the SAT instance
			if len([P[k][j] for k in range(max_lines) if P[k][j] == 'T']) != 11:
				continue

			generate_clause(S)

# Generate clauses that say that every light line intersects with every heavy and medium line
for i in range(21):
	for j in range(21, max_lines):
		# Ignore the case when line i and j already intersect
		if lines_intersect(i, j):
			continue

		# Find set of possible intersections
		S = {P[j][k] for k in usecols if P[i][k] == 'T' and type(P[j][k]) == int}

		# Ignore the case when line i has intersections after the maximum column in the SAT instance
		if len([P[i][k] for k in usecols if P[i][k] == 'T']) != 11:
			continue

		generate_clause(S)

# Output SAT instance in DIMACS format
print "p cnf {0} {1}".format(111*(max_lines-1)+max_columns, len(clauses))
for clause in clauses:
	print clause

