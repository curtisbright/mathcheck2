# Generate clauses derived from the "partial isomorphism removal" property of (Lam et al. 1989)
import itertools
import copy

if not 'A' in vars():
	print "This script should only be used from within the script that generates clauses from a given A2"
	quit()

# Dictionary that provides the case # of a given A1
execfile("data/a1s.data")

# Dictionary that provides the order in which each case is solved
# Cases have been ordered by how many A2 instances occur in each case; explicitly, the cases are solved in the following order:
# 46,60,66,53,63,39,34,65,56,48,47,50,42,27,3,37,18,55,51,58,43,36,11,23,16,17,41,12,13,7,33,24,22,26,25,15,9
# Cases that are solved first have small rank, cases that are ruled out have negative rank, and cases for which the removal property does not apply do not appear at all
caserank = {32: -1, 64: -1, 35: -1, 4: -1, 38: -1, 40: -1, 10: -1, 44: -1, 45: -1, 14: -1, 61: -1, 19: -1, 52: -1, 62: -1, 54: -1, 57: -1, 59: -1, 28: -1, 29: -1, 30: -1, 31: -1, 4: -1, 10: -1, 14: -1, 65: 7, 66: 2, 3: 14, 7: 29, 9: 36, 11: 22, 12: 27, 13: 28, 15: 35, 16: 24, 17: 25, 18: 16, 22: 32, 23: 23, 24: 31, 25: 34, 26: 33, 27: 13, 33: 30, 34: 6, 36: 21, 37: 15, 39: 5, 41: 26, 42: 12, 43: 20, 46: 0, 47: 10, 48: 9, 50: 11, 51: 18, 53: 3, 55: 17, 56: 8, 58: 19, 60: 1, 63: 4}

r1s = []
r2s = []
newrows = []
newcols = []
matrixlist = []
unknownlist = []

def to_str(A):
	st = ""
	for i in range(6):
		for j in range(19):
			st += str(A[i][j])
		st += "\n"
	return st

# Determine which of the first six rows intersect and the rows/columns that contain the A1 induced by the partial isomorphism removal criterion
for r1 in range(6):
	for r2 in range(r1+1,6):
		does_intersect = False
		for col in range(19):
			if A[r1][col]=='1' and A[r2][col]=='1':
				does_intersect = True
		if not does_intersect and b[r1]=='1' and b[r2]=='1':
			# Rows r1 and r2 intersect outside of the first 19 columns so the partial isomorphism removal criterion applies
			r1s.append(r1)
			r2s.append(r2)
			newrows.append([])
			newcols.append([])
			matrixlist.append([[0 for j in range(19)] for i in range(6)])
			unknownlist.append([])
			# Find the columns that contain the induced A1
			for col in range(max_columns):
				if (int(A[r1][col])+int(A[r2][col])+(1 if col<19 else 0))%2 == 1:
					newcols[-1].append(col)
			# Find the rows that contain the induced A1
			for r in range(43):
				# Determine how many 1s appear in the induced columns of row r
				count = 0
				for col in newcols[-1]:
					if A[r][col]=='1':
						count += 1

				# If five 1s appear in the induced columns of row r then the induced A1 includes this row
				if count == 5:
					newrows[-1].append(r)
				# At least three points must already be known in the rows of the induced A1
				elif count >= 3:
					r1_r2_intersect_count = 0
					for j in range(19):
						if A[r][j]=='1':
							r1_r2_intersect_count += sum([int(A[i][j]) for i in [r1, r2]])
					# Check if row r must have intersections in blocks r1 and r2
					if r1_r2_intersect_count == 0:
						# Find lists of unknown entries in row r that appear in the induced A1
						for s in [r1, r2]:
							newunknownlist = [100*len(newrows[-1])+col for col in range(19) if A[s][newcols[-1][col]]=='1' and A[r][newcols[-1][col]]==' ']
							if newunknownlist != []:
								unknownlist[-1].append(newunknownlist)
						newrows[-1].append(r)

			# The induced A1 must have 6 rows and 19 columns
			assert(len(newrows[-1])==6 and len(newcols[-1])==19)

			# Form incidence matrix using the known entries of the induced A1
			for r in range(6):
				for col in range(19):
					if A[newrows[-1][r]][newcols[-1][col]]=='1':
						matrixlist[-1][r][col] = 1

# Check if a 6 by 19 incidence matrix is not a valid A1, either because it contains two lines
# that intersect twice or doesn't contain five 1s on each row
def invalid_case(A):
	for i1 in range(6):
		for i2 in range(i1+1,6):
			if sum([A[i1][j]*A[i2][j] for j in range(19)]) > 1:
				return True
		if sum(A[i1]) != 5:
			return True
	return False

# Sort the columns of the A1 incidence matrix
def sort_columns(A):
	A2 = [[A[i][j] for i in range(6)] for j in range(19)]
	A2.sort(reverse=True)
	return [[A2[j][i] for j in range(19)] for i in range(6)]

# Convert an A1 incidence matrix to a string containing the true literals in its SAT representation
def to_integer_string(A):
	# Ensure that both the columns and rows of A are sorted
	while True:
		B = sorted(A, reverse=True)
		C = sort_columns(B)
		if A == B == C:
			break
		A = C
	st = ""
	for r in range(6):
		for c in range(19):
			if A[r][c] == 1:
				st += str(100*(r+1)+c+1)+" "
	return st[:-1]

# Apply the partial isomorphism removal criterion for each pair of the first six rows that intersect
for i in range(len(matrixlist)):
	totalpossiblecases = 0
	totalblockedcases = 0
	# Try all possibilities for completing the undetermined rows
	for element in itertools.product(*unknownlist[i]):
		matrix = copy.deepcopy(matrixlist[i])
		# Complete the undetermined rows and form the incidence matrix of this possibility
		for e in element:
			r = e/100
			col = e%100
			matrix[r][col] = 1

		# Ignore if this case if the matrix is not a valid A1
		if invalid_case(matrix):
			continue

		# Determine the case of the induced A1 in this possibility
		case = a1s[to_integer_string(matrix)]

		totalpossiblecases += 1
		# If this A1 is one that has already been solved then we can learn a blocking clause as it is known to not lead to a solution
		if caserank[case] < caserank[c]:
			totalblockedcases += 1
			#print "c Learning conflict clause (case {0} is solved before case {1})".format(case, c)
			conflict = set()
			for e in element:
				r = newrows[i][e/100]
				col = newcols[i][e%100]
				conflict.add(var(r,col))
			generate_negative_clause(conflict)
			if len(element)==1:
				A[r][col] = '0'

	# If all cases have been blocked using partial isomorphism removal
	if totalpossiblecases == totalblockedcases:
		print "0"
		if print_info:
			print_a2()
		print "c {0} blocks, {1} cols, {2} vars; Case ruled out by partial isomorphism removal".format("".join(b), max_columns, total_vars)
		quit()
