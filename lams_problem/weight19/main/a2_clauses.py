# Script to generate the clauses that can be dervied from a given A2

import sys

# Option to print a string containing the positive unit clauses used in the SAT encoding of the A2 instance
if "-print-a2-string" in sys.argv:
	print_a2_string = True
	sys.argv.remove("-print-a2-string")
	a2_string = "a "
else:
	print_a2_string = False

# Option to print information about the A2 instance
if "-print-info" in sys.argv:
	print_info = True
	sys.argv.remove("-print-info")
else:
	print_info = False

# Option to turn off the partial isomorphism removal clauses
if "-no-partial-removal" in sys.argv:
	use_partial_isomorphism_removal = False
	sys.argv.remove("-no-partial-removal")
else:
	use_partial_isomorphism_removal = True

if len(sys.argv) <= 3:
	print "Need case #, block selection pattern, and A2 instance #"
	quit()

# Return the variable number corresponding to the (i, j)th entry of A
# where 0 <= i < 111 denotes the row and 0 <= j < 100 denotes the column (last 11 columns unused)
def var(i,j):
	return 100*(i+1)+j+1

# Generate a clause specifying (x1 & ... & xn) -> (y1 | ... | yk)
# where X = {x1, ..., xn} and Y = {y1, ..., yk}
def generate_implication_clause(X, Y):
	if 'F' in X or 'T' in Y:
		return
	clause = ""
	for x in sorted(X - {'T'}):
		clause += str(-x) + " "
	for y in sorted(Y - {'F'}):
		clause += str(y) + " "
	clause += "0"
	clauses.append(clause)

def print_a2():
	for i in range(43):
		st = "c "
		for j in range(max_columns):
			st += A[i][j]
		print st

# Generate a clause containing the positive literals of the variables in the set X
def generate_clause(X):
	global a2_string
	if 'T' in X or X==set([]):
		return
	clause = ""
	for x in sorted(X - {'F'}):
		clause += str(x) + " "
	if print_a2_string:
		# A2 string should only consist of unit clauses
		assert(len(X)==1)
		a2_string += clause
	else:
		clause += "0"
		clauses.append(clause)

# Generate a clause containing the negative literals of the variables in the set X
def generate_negative_clause(X):
	if 'F' in X:
		return
	clause = ""
	for x in sorted(X - {'T'}):
		clause += str(-x) + " "
	if not print_a2_string:
		clause += "0"
		clauses.append(clause)

c = int(sys.argv[1])
b = list(sys.argv[2])
n = int(sys.argv[3])

if len(b) != 7:
	print "Block selection pattern must be a {0,1} string of length 7 representing which blocks to use"
	quit()

# Set initial entries
f = open("../a2/initial/{0}.initial".format(c), "r")
A = []
lines = f.readlines()
for line in lines:
	A.append(list(line[:-1]))
f.close()

clauses = []
total_vars = 11200
max_lines = 111
inside_columns = len(A[0])

# Determine the columns which contain intersections between the first six rows
intersecting_columns = 19
while sum([int(A[i][intersecting_columns]) for i in range(6)]) == 2:
	intersecting_columns += 1

# The rows of A2 will use a custom sort so clear these rows
for i in range(6,43):
	for j in set(range(inside_columns))-set(range(19, intersecting_columns)):
		A[i][j] = ' '

f = open("a2s/{0}.complete".format(c), "r")

line = f.readlines()[n][2:-3]
for x in line.split(" "):
	row = (abs(int(x))/100)-1
	col = (abs(int(x))%100)-1
	if int(x)>0:
		A[row][col] = '1'
	else:
		A[row][col] = '0'
f.close()

# Choose a column to sort the rows of A2 by
sorting_column = 18
# Set to hold up to 4 blocks that intersect another block
intersecting_blocks = set()
# List of the eight cases with the hardest instances
cases_with_no_block_intersections = [1, 2, 5, 6, 8, 20, 21, 49]

if c in cases_with_no_block_intersections:
	# Partial isomorphism removal does not apply in these cases
	use_partial_isomorphism_removal = False
else:
	# Get block selection order
	with open("data/{0}.order".format(c), "r") as f:
		lines = f.readlines()
	block_order = [int(lines[i][2])-1 for i in range(6)]
	for i in range(18,-1,-1):
		if sum([int(A[block_order[k]][i]) for k in range(4)])==0 and sum([int(A[block_order[k]][i]) for k in range(4,6)])<=1:
			sorting_column = i
			break
	for i in range(19,intersecting_columns):
		for k in range(4):
			if A[block_order[k]][i] == '1':
				intersecting_blocks.add(block_order[k])

def charrev(x):
	if x==' ':
		return '1'
	if x=='1':
		return '0'

Asort = [[A[j][i] for i in range(inside_columns)] for j in range(43)]
for i in range(43):
	Asort[i] = [charrev(Asort[i][sorting_column])] + [-1] + [-1] + Asort[i]

for i in range(6,43):
	intersections = [0,0,0,0,0,0]
	for j in range(19):
		for k in range(6):
			if A[i][j]=='1' and A[k][j]=='1':
				intersections[k] = 1
	Asort[i][1] = sum([intersections[k] for k in range(6)])
	for j in set(range(6))-intersecting_blocks:
		intersections[j] = 0
	Asort[i][2] = sum([intersections[k] for k in range(6)])

Asort.sort()

# Set entries of A2
for i in range(6,43):
	for j in range(19):
		A[i][j] = Asort[i][j+3]
		if A[i][j]=='1':
			generate_clause({var(i, j)})
		else:
			A[i][j]='0'
			generate_negative_clause({var(i, j)})

# If outside block used compute how many columns it should contain
if b[6] == '1':
	inside_points_on_special_line = 9
	for j in range(19):
		if A[6][j]=='1':
			inside_points_on_special_line -= sum([int(A[i][j]) for i in range(6)])

	max_columns = inside_columns + (11-inside_points_on_special_line)
	while len(A[0]) < max_columns:
		for i in range(6):
			A[i].append('0')
		for i in range(6, max_lines):
			A[i].append(' ')

	# Set the initial points on the outside block
	for j in range(inside_columns, max_columns):
		A[6][j] = '1'
else:
	max_columns = inside_columns

# Determine the columns that appear in each block and those to be used in the instance
usedcols = []
blocks = [[],[],[],[],[],[],[]]

for i in range(7):
	for j in range(19,max_columns):
		if A[i][j] == '1':
			if b[i] == '1' and not j in usedcols:
				usedcols += [j]
			if sum([int('0'+A[ii][j]) for ii in range(7)]) <= 1:
				blocks[i] += [j]

for i1 in range(43):
	for i2 in range(i1+1, 43):
		for j1 in range(19):
			for j2 in range(19,max_columns):
				if A[i1][j1] == '1' and A[i1][j2] == '1' and A[i2][j1] == '1' and A[i2][j2] == ' ':
					A[i2][j2] = '0'
					generate_negative_clause({var(i2, j2)})

for i in range(7):
	if blocks[i] == [] or not(blocks[i][0] in usedcols):
		continue
	blocklen = len(blocks[i])
	rows = [k for k in range(43) if A[k][blocks[i][0]] == ' ']
	for j in range(blocklen):
		for k in range(j+1,blocklen):
			A[rows[j]][blocks[i][k]] = '0'
			generate_negative_clause({var(rows[j], blocks[i][k])})
	if i < 6:
		assert(len(rows)==2*blocklen)
		A[rows[0]][blocks[i][0]] = '1'
		generate_clause({var(rows[0], blocks[i][0])})

# Assign some entries whose values are forced
for i1 in range(6,43):
	for i2 in range(i1+1, 43):
		for j1 in range(19):
			for j2 in range(19,max_columns):
				if A[i1][j1] == '1' and A[i1][j2] == '1' and A[i2][j1] == '1' and A[i2][j2] == ' ':
					A[i2][j2] = '0'
					generate_negative_clause({var(i2, j2)})
					for i in range(6):
						if A[i][j2]=='1':
							break
					cols = [k for k in blocks[i] if A[i2][k] == ' ']
					if len(cols)==1:
						A[i2][cols[0]] = '1'
						generate_clause({var(i2, cols[0])})

if print_a2_string:
	print a2_string
	if print_info:
		print_a2()
	quit()

# Generate clauses that say the first 19 columns intersect with the later used columns
for j1 in range(19):
	for j2 in usedcols:
		if j2 > j1:
			rows = [i for i in range(max_lines) if A[i][j1] == '1']
			if len(rows) != 11:
				continue
			if '1' in [A[i][j2] for i in rows]:
				continue
			generate_clause({var(i,j2) for i in rows if A[i][j2] == ' '})

for r in range(7):
	for col in blocks[r]:
		if not col in usedcols:
			continue
		# List 'rows' contains the unassigned variables in the first 43 columns of column col
		rows = [k for k in range(6,43) if A[k][col] == ' ']
		rows1 = [k for k in range(6,43) if A[k][col] == '1']
		if len(rows1) == 2 and r < 6:
			# Sum of entries in 'rows' is 0 in this case
			for i in rows:
				A[i][col] = '0'
				generate_negative_clause({var(i, col)})
		else:
			# Sum of entries in 'rows' is at least 1 in this case
			generate_clause({var(i, col) for i in rows})
		if len(rows1) == 1 and r < 6:
			# Sum of entries in 'rows' is at most 1 in this case
			for i1 in range(len(rows)):
				for i2 in range(i1+1, len(rows)):
					generate_negative_clause({var(rows[i1], col), var(rows[i2], col)})

		# Inside block
		if r < 6:
			if len(rows1) == 0:
				# Naive formulation of cardinality constraint 'at most 2'
				for i1 in range(len(rows)):
					for i2 in range(i1+1, len(rows)):
						for i3 in range(i2+1, len(rows)):
							generate_negative_clause({var(rows[i1], col), var(rows[i2], col), var(rows[i3], col)})

				# Lexicographical column ordering
				if col+1 in blocks[r]:
					rowsnext = [k for k in range(6,43) if A[k][col+1] == ' ']
					for i1 in rows:
						for i2 in rows:
							if i2 < i1:
								for i3 in rowsnext:
									if i3 < i2:
										generate_negative_clause({var(i1,col), var(i2,col), var(i3,col+1)})

			rows.reverse()
			rowlen = len(rows)
			if len(rows1) == 0:
				# Sum of entries in 'rows' is exactly 2 in this case; use sequential counter encoding
				counter_len = 4
				S = [[0 for j in range(counter_len)] for i in range(rowlen+1)]

				for i in range(rowlen+1):
					S[i][0] = 'T' # True
				for j in range(1,counter_len):
					S[0][j] = 'F' # False
				S[rowlen][2] = 'T' # True
				S[rowlen][counter_len-1] = 'F' # False

				for i in range(rowlen+1):
					for j in range(counter_len):
						if S[i][j] == 0:
							S[i][j] = total_vars
							total_vars += 1

				for i in range(1, rowlen+1):
					for j in range(1,counter_len):
						generate_implication_clause({S[i-1][j]}, {S[i][j]})
						generate_implication_clause({var(rows[i-1], col), S[i-1][j-1]}, {S[i][j]})
						generate_implication_clause({S[i][j]}, {S[i-1][j], var(rows[i-1], col)})
						generate_implication_clause({S[i][j]}, {S[i-1][j], S[i-1][j-1]})

				if col+1 in blocks[r]:
					rowsnext = [k for k in range(6,43) if A[k][col+1] == ' ']
					for i in range(1, rowlen):
						for j in rowsnext:
							if j < rows[i]:
								# Follows by lexicographic ordering
								generate_negative_clause({S[i+1][2], var(j, col+1)})

		# Outside block
		elif r == 6:
			assert(len(rows1)==1)
			rows.reverse()
			rowlen = len(rows)

			# Sum of entries in 'rows' is exactly 3 in this case; use sequential counter encoding
			counter_len = 5
			S = [[0 for j in range(counter_len)] for i in range(rowlen+1)]

			for i in range(rowlen+1):
				S[i][0] = 'T' # True
			for j in range(1,counter_len):
				S[0][j] = 'F' # False
			S[rowlen][3] = 'T' # True
			S[rowlen][counter_len-1] = 'F' # False

			for i in range(rowlen+1):
				for j in range(counter_len):
					if S[i][j] == 0:
						S[i][j] = total_vars
						total_vars += 1

			for i in range(1, rowlen+1):
				for j in range(1,counter_len):
					generate_implication_clause({S[i-1][j]}, {S[i][j]})
					generate_implication_clause({var(rows[i-1], col), S[i-1][j-1]}, {S[i][j]})
					generate_implication_clause({S[i][j]}, {S[i-1][j], var(rows[i-1], col)})
					generate_implication_clause({S[i][j]}, {S[i-1][j], S[i-1][j-1]})

			if col+1 in blocks[r]:
				rowsnext = [k for k in range(6,43) if A[k][col+1] == ' ']
				for i in range(1, rowlen):
					for j in rowsnext:
						if j < rows[i]:
							# Follows by lexicographic ordering
							generate_negative_clause({S[i+1][3], var(j, col+1)})

			# Naive formulation of cardinality constraint 'at most 3'
			for i1 in range(len(rows)):
				for i2 in range(i1+1, len(rows)):
					for i3 in range(i2+1, len(rows)):
						for i4 in range(i3+1, len(rows)):
							generate_negative_clause({var(rows[i1], col), var(rows[i2], col), var(rows[i3], col), var(rows[i4], col)})

			# Lexicographical column ordering
			if col+1 in blocks[r]:
				rowsnext = [k for k in range(6,43) if A[k][col+1] == ' ']
				for i1 in rows:
					for i2 in rows:
						for i3 in rows:
							if i3 < i2 and i2 < i1:
								for i4 in rowsnext:
									if i4 < i3:
										generate_negative_clause({var(i1,col), var(i2,col), var(i3,col), var(i4,col+1)})

# Partial isomorphism removal clauses are optional (enabled by default)
if use_partial_isomorphism_removal:
	execfile("partial_isomorphism_clauses.py")
	
# If outside block used generate clauses that the special row intersects all later rows
if b[6]=='1':
	cols = [j for j in range(max_columns) if A[6][j] == '1']
	if len(cols)==11:
		for i in range(max_lines):
			if '1' in [A[i][j] for j in cols]:
				continue
			generate_clause({var(i, j) for j in cols if A[i][j] == ' '})

for clause in clauses:
	print clause

if print_info:
	print_a2()

print "c {0} blocks, {1} cols, {2} vars".format("".join(b), max_columns, total_vars)
