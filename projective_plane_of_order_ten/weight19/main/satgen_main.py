# Script to generate the main SAT instance for a given case and A2 instance

import sys

# Option to turn off lexicographic ordering clauses
if "-no-lex" in sys.argv:
	nolex = True
	sys.argv.remove("-no-lex")
else:
	nolex = False

# Option to print information about the instance instead of the SAT clauses
if "-print-info" in sys.argv:
	print_info = True
	sys.argv.remove("-print-info")
else:
	print_info = False

# Option to fix the known zeros (by lexicographically ordering the rows) by using unit clauses
# These may be useful but are disabled by default as we did not use them in our results
if "-lex-zeros" in sys.argv:
	lex_zeros = True
	sys.argv.remove("-lex-zeros")
else:
	lex_zeros = False

# Return the variable number corresponding to the (i, j)th entry of A
# where 0 <= i < 111 denotes the row and 0 <= j < 100 denotes the column (last 11 columns unused)
def var(i, j):
	return 100*(i+1)+j+1

if len(sys.argv) <= 2:
	print "Need case # and block selection pattern (and the maximum column to use if an outside block is used)"
	quit()

case = int(sys.argv[1])
useblocks = list(sys.argv[2])

if case in [4, 10, 14, 19, 28, 29, 30, 31, 35, 40, 44, 45, 59, 61, 62]:
	print "Case ruled out because no A2s exist in this case"
	quit()

if case in [32, 38, 54, 57, 64]:
	print "Case ruled out because it implies the existence of a weight 16 word in the rowspace of A"
	quit()

if case == 52:
	print "Case ruled out by theoretical argument (Lam, Crossfield, and Thiel 1985)"
	quit()

if len(useblocks) != 7:
	print "Block selection pattern must be a {0,1} string of length 7 representing which blocks to use"
	quit()

# Set initial entries
f = open("../a2/initial/{0}.initial".format(case), "r")
lines = f.readlines()
A = []
for line in lines:
	A.append(list(line[:-1]))
f.close()

clauses = []
known_lines = 6
max_lines = 111
inside_columns = len(A[0])
total_vars = 11200

# Add extra columns if necessary
if useblocks[6] == '1':
	if len(sys.argv) < 4:
		print "Need to specify how many columns to use"
		quit()
	max_columns = int(sys.argv[3])
	while len(A[0]) < max_columns:
		for i in range(6):
			A[i].append('0')
		for i in range(6, max_lines):
			A[i].append(' ')
else:
	max_columns = inside_columns

# Determine the columns which contain intersections between the first six rows
intersecting_columns = 19
while sum([int(A[i][intersecting_columns]) for i in range(6)]) == 2:
	intersecting_columns += 1

# The rows of A2 will use a custom sort so clear these rows
for i in range(6,43):
	for j in set(range(max_columns))-set(range(19, intersecting_columns)):
		A[i][j] = ' '

# Set the initial points on the outside block
for j in range(inside_columns, max_columns):
	A[6][j] = '1'

# Generate variables for undetermined entries of A and represent known entries by 'T' or 'F'
for i in range(max_lines):
	for j in range(max_columns):
		if len(A[i]) <= j:
			A[i].append(var(i, j))
		elif A[i][j] == '0':
			clauses.append("-{0} 0".format(var(i, j)))
			A[i][j] = 'F'
		elif A[i][j] == '1':
			clauses.append("{0} 0".format(var(i, j)))
			A[i][j] = 'T'
		elif A[i][j] == ' ':
			A[i][j] = var(i, j)

# Compute list of rows and columns to use in the SAT instance
used_rows = []
for i in range(6):
	if useblocks[i] == '1':
		used_rows.append(i)

used_columns = range(19)
for j in range(19, intersecting_columns):
	for i in used_rows:
		if A[i][j] == 'T':
			if not j in used_columns:
				used_columns.append(j)
			break

for i in used_rows:
	for j in range(intersecting_columns, max_columns):
		if A[i][j] == 'T' and not j in used_columns:
			used_columns.append(j)

used_columns += range(inside_columns, max_columns)
used_rows += range(6, max_lines)

# Generate a clause containing the positive literals of the variables in the set X
def generate_clause(X):
	if 'T' in X or X==set([]):
		return
	clause = ""
	for x in sorted(X - {'F'}):
		clause += str(x) + " "
	clauses.append(clause + "0")

# Generate a clause containing the negative literals of the variables in the set X
def generate_negative_clause(X):
	if 'F' in X:
		return
	clause = ""
	for x in sorted(X - {'T'}):
		clause += str(-x) + " "
	clauses.append(clause + "0")

if not print_info:
	# Generate clauses that say that any two distinct rows do not intersect twice
	for i in used_rows:
		for j in range(max(6, i+1), max_lines):
			for k in used_columns:
				for l in used_columns:
					if l > k:
						generate_negative_clause({A[i][k], A[j][k], A[i][l], A[j][l]})

	# Generate clauses that say the first six rows intersect all later rows
	for i in range(6):
		if not i in used_rows:
			continue
		for j in range(6, max_lines):
			# Find set of possible intersection entries
			S = {A[j][k] for k in used_columns if A[i][k] == 'T'}

			# Row i must be entirely known
			assert(len([A[i][k] for k in used_columns if A[i][k] == 'T']) == 11)

			generate_clause(S)

	# Generate clauses that say that every totally known column intersects every used column
	for i in range(19, intersecting_columns):
		for j in used_columns:
			# Ignore first 19 columns as they will be completed by an A2
			if j < 19:
				continue

			# Find set of possible intersection entries
			S = {A[k][j] for k in range(max_lines) if A[k][i] == 'T'}

			# Ignore cases where column i is not entirely known
			if len([A[k][i] for k in range(max_lines) if A[k][i] == 'T']) != 11:
				continue

			generate_clause(S)

# Generate the lexicographic ordering clauses if they have been enabled
if nolex == False:
	# Get the ordering of blocks 1-6 to use in the lexicographic clauses
	order_rows = []
	f = open("data/{0}.order".format(case), 'r')
	for line in f.readlines()[0:6]:
		order_rows.append(int(line.split(" ")[1])-1)
	f.close()
	# Outside block has least priority when deciding which block to apply the lexicographic ordering to
	order_rows.append(6)

	# Lexicographically order the bottom rows
	for i in range(43, max_lines-1):
		if lines[i] == lines[i+1]:
			lex_ordered = False
			for j in order_rows:
				S1 = [A[i][k] for k in used_columns if A[j][k] == 'T' and type(A[i][k]) == int]
				S2 = [A[i+1][k] for k in used_columns if A[j][k] == 'T' and type(A[i+1][k]) == int]
				if S1 == []:
					continue
				for k in range(len(S1)):
					for k2 in range(k):
						generate_negative_clause({S1[k], S2[k2]})
				lex_ordered = True
				break
			if not lex_ordered:
				print "c Line {0} was not lex ordered as not enough blocks selected".format(i+1)

	# Fix known zeros using unit clauses if that option was enabled
	if lex_zeros:
		inc = 0
		for i in range(43, max_lines):
			if i != max_lines-1 and lines[i] == lines[i+1]:
				for j in order_rows:
					S = [k for k in used_columns if A[j][k] == 'T' and type(A[i][k]) == int]
					if S == []:
						continue
					for k in S[:inc]:
						generate_negative_clause({A[i][k]})
						A[i][k] = 'F'
					break
				inc += 1
			else:
				for j in order_rows:
					S = [k for k in used_columns if A[j][k] == 'T' and type(A[i][k]) == int]
					if S == []:
						continue
					for k in S[:inc]:
						generate_negative_clause({A[i][k]})
						A[i][k] = 'F'
					break
				inc = 0

		inc = 0
		for i in range(max_lines-1, 42, -1):
			if i != 43 and lines[i] == lines[i-1]:
				for j in order_rows:
					S = [k for k in used_columns if A[j][k] == 'T' and type(A[i][k]) == int]
					if S == []:
						continue
					for k in S[len(S)-inc:]:
						generate_negative_clause({A[i][k]})
						A[i][k] = 'F'
					break
				inc += 1
			else:
				for j in order_rows:
					S = [k for k in used_columns if A[j][k] == 'T' and type(A[i][k]) == int]
					if S == []:
						continue
					for k in S[len(S)-inc:]:
						generate_negative_clause({A[i][k]})
						A[i][k] = 'F'
					break
				inc = 0

# Print information about SAT instance if that option was enabled
if print_info:
	print "c intersecting columns:", intersecting_columns-19
	print "c inside columns:", inside_columns
	print "c max columns:", max_columns
	print "c used rows:", used_rows
	print "c used columns:", used_columns
	for i in range(max_lines):
		st = "c "
		for j in range(max_columns):
			if A[i][j]=='T':
				st += "1"
			elif A[i][j]=='F':
				st += "0"
			else:
				st += " "
		print st
	quit()

# Output SAT instance in DIMACS format
print "p cnf {0} {1}".format(total_vars, len(clauses))
for clause in clauses:
	print clause

