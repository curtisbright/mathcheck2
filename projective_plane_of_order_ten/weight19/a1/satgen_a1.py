# Script to generate the A1 SAT instance

# Return the variable number corresponding to the (i, j)th entry of A
# where 0 <= i < 111 denotes the row and 0 <= j < 100 denotes the column (last 11 columns unused)
def var(i, j):
	return 100*(i+1)+j+1

clauses = []
max_row = 6
max_column = 19	
total_vars = var(max_row, max_column)

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

	clauses.append("-{0} {1} 0".format(X[0], Y[0]))
	clauses.append("-{0} {1} 0".format(X[0], total_vars+1))
	clauses.append("{0} {1} 0".format(Y[0], total_vars+1))
	for k in range(1, n-1):
		clauses.append("-{0} {1} -{2} 0".format(X[k], Y[k], total_vars+k))
		clauses.append("-{0} {1} -{2} 0".format(X[k], total_vars+k+1, total_vars+k))
		clauses.append("{0} {1} -{2} 0".format(Y[k], total_vars+k+1, total_vars+k))
	clauses.append("-{0} {1} -{2} 0".format(X[n-1], Y[n-1], total_vars+n-1))

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
for i in range(max_row):
	for j in range(i+1, max_row):
		for k in range(max_column):
			for l in range(k+1, max_column):
				generate_negative_clause({var(i,k), var(j,k), var(i,l), var(j,l)})

# Generate clauses that say there are 5 points on each line
for i in range(max_row):
	S = [var(i,j) for j in range(max_column)]
	generate_adder_clauses(S, 5)

# Generate clauses that say that columns are lexicographically ordered
for j in range(max_column-1):
	S1 = [var(i,j) for i in range(max_row)]
	S2 = [var(i,j+1) for i in range(max_row)]
	generate_lex_clauses(S2, S1)

# Generate clauses that say that rows are lexicographically ordered
for i in range(max_row-1):
	S1 = [var(i,j) for j in range(max_column)]
	S2 = [var(i+1,j) for j in range(max_column)]
	generate_lex_clauses(S2, S1)

# Output SAT instance in DIMACS format
print "p cnf {0} {1}".format(total_vars, len(clauses))
for clause in clauses:
	print clause
