# Weight 16 SAT generation script

import sys, os.path

if len(sys.argv) <= 1:
	print "Need case of SAT instance to generate (1a, 1b, 1c, 2, 3, 4, 5, 6a, 6b, 6c)"
	quit()

if not sys.argv[1] in ["1a", "1b", "1c", "2", "3", "4", "5", "6a", "6b", "6c"]:
	print "Invalid case (need one of 1a, 1b, 1c, 2, 3, 4, 5, 6a, 6b, 6c)"
	quit()

# Initial assignment to the values of P where blanks signify undetermined entries
with open("initial/initial_matrix_{0}".format(sys.argv[1])) as f:
	initial_P = f.read()

# Convert initial assignment from a string to a matrix
P = []
for row in initial_P.split('\n'):
	P.append(list(row))

print_matrix = False
remove_blocks = True

# Total number of lines to use
max_columns = len(P[0]) if len(sys.argv) <= 2 else int(sys.argv[2])
max_lines = 80
lex_vars = 111*(max_lines-1)+max_columns
special_line = 0 if len(sys.argv) <= 3 else int(sys.argv[3])

if special_line != 0:
	for i in range(8, max_lines):
		for j in range(max_columns-5, max_columns):
			if i == special_line:
				P[i][j] = '1'
			else:
				P[i][j] = ' '

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
	X = sorted(X - {'F'})
	for x in X:
		clause += str(x) + " "
	clauses.append(clause + "0")

# Generate a clause containing the negative literals of the variables in the set X
def generate_negative_clause(X):
	if 'F' in X:
		return
	clause = ""
	X = sorted(X - {'T'})
	for x in X:
		clause += str(-x) + " "
	clauses.append(clause + "0")

# Fill in entries that are forced to be false
for i in range(max_lines):
	for j in range(i+1, max_lines):
		for k in range(max_columns):
			for l in range(k+1, max_columns):
				if P[i][k]=='1' and P[i][l]=='1' and P[j][k]=='1':
					P[j][l] = '0'
				if P[i][k]=='1' and P[i][l]=='1' and P[j][l]=='1':
					P[j][k] = '0'
				if P[i][k]=='1' and P[j][l]=='1' and P[j][k]=='1':
					P[i][l] = '0'
				if P[j][l]=='1' and P[i][l]=='1' and P[j][k]=='1':
					P[i][k] = '0'

# Generate variables for undetermined entries of P and represent known entries by 'T' or 'F'
for i in range(max_lines):
	for j in range(max_columns):
		if j >= len(P[i]):
			P[i].append(' ')
		if P[i][j] == '0':
			P[i][j] = 'F'
			clauses.append("-{0} 0".format(var(i, j)))
		elif P[i][j] == '1':
			P[i][j] = 'T'
			clauses.append("{0} 0".format(var(i, j)))
		elif P[i][j] == ' ':
			P[i][j] = var(i, j)

if print_matrix:
	for i in range(max_lines):
		st = ""
		for j in range(max_columns):
			st += "0" if P[i][j] == 'F' else "1" if P[i][j] == 'T' else " "
		print st
	quit()

# Generate clauses that say that any two distinct lines do not intersect twice
for i in range(max_lines):
	for j in range(i+1, max_lines):
		for k in range(max_columns):
			if remove_blocks and sys.argv[1]=="1c" and k in [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]:
				continue
			if remove_blocks and sys.argv[1]=="1b" and k in [39, 40, 41, 42, 43, 44]:
				continue
			if remove_blocks and sys.argv[1]=="1a" and k in [41, 42, 43, 44]:
				continue
			for l in range(k+1, max_columns):
				if remove_blocks and sys.argv[1]=="1c" and l in [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]:
					continue
				if remove_blocks and sys.argv[1]=="1b" and l in [39, 40, 41, 42, 43, 44]:
					continue
				if remove_blocks and sys.argv[1]=="1a" and l in [41, 42, 43, 44]:
					continue
				generate_negative_clause({P[i][k], P[j][k], P[i][l], P[j][l]})

# Generate clauses that say that first 16 columns intersect with remaining columns
for j in range(16):
	for i in range(16, max_columns):
		if remove_blocks and sys.argv[1]=="1c" and i in [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]:
			continue
		if remove_blocks and sys.argv[1]=="1b" and i in [39, 40, 41, 42, 43, 44]:
			continue
		if remove_blocks and sys.argv[1]=="1a" and i in [41, 42, 43, 44]:
			continue
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
for i in range(17):
	if remove_blocks and sys.argv[1]=="1c" and i in [1, 2]:
		continue
	if remove_blocks and sys.argv[1]=="1b" and i in [4]:
		continue
	if remove_blocks and sys.argv[1]=="1a" and i in [4]:
		continue
	for j in range(8, max_lines):
		# Ignore the case when line i and j already intersect
		if lines_intersect(i, j):
			continue

		# Find set of possible intersections
		S = {P[j][k] for k in range(max_columns) if P[i][k] == 'T' and type(P[j][k]) == int}

		# Ignore the case when line i has intersections after the maximum column in the SAT instance
		if len([P[i][k] for k in range(max_columns) if P[i][k] == 'T']) != 11:
			continue

		generate_clause(S)

# Generate list of identical columns
identical_cols = []
for i in range(1,max_columns):
	if remove_blocks and sys.argv[1]=="1c" and i in [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]:
		continue
	if remove_blocks and sys.argv[1]=="1b" and i in [39, 40, 41, 42, 43, 44]:
		continue
	if remove_blocks and sys.argv[1]=="1a" and i in [41, 42, 43, 44]:
		continue
	if [k for k in range(max_lines) if P[k][i] == 'T'] == [k for k in range(max_lines) if P[k][i-1] == 'T']:
		identical_cols.append(i)

# Generate clauses that lexicographically order columns that are identical
for i in identical_cols:
	prior_identical_cols = 0
	tmp_col = i
	while tmp_col-1 in identical_cols:
		prior_identical_cols += 1
		tmp_col -= 1
	next_identical_cols = 1
	tmp_col = i
	while tmp_col+1 in identical_cols:
		next_identical_cols += 1
		tmp_col += 1

	tmp_col = 0
	while points_intersect(tmp_col, i):
		tmp_col += 1

	S = [k for k in range(max_lines) if type(P[k][i]) == int and P[k][tmp_col] == 'T']

	for k in S[-next_identical_cols:]:
		P[k][i-1] = 'F'
		clauses.append("-{0} 0".format(var(k, i-1)))

	for k in S[:prior_identical_cols]:
		P[k][i-1] = 'F'
		clauses.append("-{0} 0".format(var(k, i-1)))

	if next_identical_cols == 1:
		prior_identical_cols += 1
		for k in S[:prior_identical_cols]:
			P[k][i] = 'F'
			clauses.append("-{0} 0".format(var(k, i)))

	for k in S:
		for l in S:
			if k < l:
				generate_negative_clause({P[l][i-1], P[k][i]})

# Output SAT instance in DIMACS format
print "p cnf {0} {1}".format(lex_vars, len(clauses))
for clause in clauses:
	print clause

