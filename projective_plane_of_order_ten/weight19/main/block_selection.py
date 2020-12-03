# Script to choose a selection of blocks using a heuristic method that tends to work relatively well
# 
# Given a case # and A2 instance # it outputs a single line containing three values separated by spaces:
# 1. A {0,1} string of length 7 representing which of the blocks (six inside and one outside) selected
# 2. The maximum column index used in the selected blocks
# 3. The number of inside blocks that were selected (prior to dropping one if applicable)

import sys

def num_used_blocks(X):
	return sum(map(int, list(X)))

if len(sys.argv) <= 2:
	print "Need case # and A2 instance #"
	quit()

c = int(sys.argv[1])
n = int(sys.argv[2])

# Easiest cases: more than two blocks intersect in first six rows
if c in [11,16,17,18,23,26,27,33,34,36,37,39,41,42,43,46,47,48,51,53,55,56,58,60,63,65,66]:
	if c in [53, 60, 63, 66]:
		cols = 51
	elif c in [27, 34, 39, 42, 43, 46, 47, 48, 56, 58, 65]:
		cols = 52
	elif c in [11, 16, 17, 18, 23, 26, 33, 36, 37, 41, 51, 55]:
		cols = 53

	if c in [43, 47, 53, 58, 63]:
		blocks = "0111110"
	elif c in [17, 27, 33, 34, 39, 46, 55, 56]:
		blocks = "1011110"
	elif c in [23, 51]:
		blocks = "1101110"
	elif c in [11, 16, 18, 26, 36, 37, 41, 42, 48, 65, 66]:
		blocks = "1110110"
	elif c in [60]:
		blocks = "1111010"

	numblocks = 5

	print blocks, cols, numblocks
	quit()
# Harder cases: exactly two blocks intersect in first six rows
elif c in [3,7,9,12,13,15,22,24,25,50]:
	cols = 54
# Hardest cases: no blocks intersect in first six rows
elif c in [1,2,5,6,8,20,21,49]:
	cols = 55
else:
	print "Invalid case #"
	quit()

# Set initial entries
f = open("../a2/initial/{0}.initial".format(c), "r")
A = []
lines = f.readlines()
for line in lines:
	A.append(list(line[:-1]))
f.close()

# The rows of A2 will use a custom sort so clear these rows
for i in range(6,43):
	for j in range(cols):
		A[i][j] = ' '

# Set entries of A2
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

with open("data/{0}.order".format(c), "r") as f:
	lines = f.readlines()

block_order = [int(lines[i][2])-1 for i in range(6)]
firstcols = [int(lines[k].split(" ")[2])-1 for k in range(6)]

# Choose a column to sort the rows of A2 by
for i in range(18,-1,-1):
	if A[block_order[0]][i]=='0' and A[block_order[1]][i]=='0':
		sorting_column = i
		break

# Determine the pair of blocks (if any) that intersect in the first six rows
intersecting_blocks = set()
if A[block_order[0]][19] == '1' and A[block_order[1]][19] == '1':
	intersecting_blocks = set([block_order[0], block_order[1]])

def charrev(x):
	if x==' ':
		return '1'
	if x=='1':
		return '0'

Asort = [[A[j][i] for i in range(cols)] for j in range(43)]
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

for i in range(6,43):
	for j in range(19):
		A[i][j] = Asort[i][j+3]

special_line = Asort[6][3:22]

b = list("111111")

for i in range(19):
	if special_line[i] == '1':
		for j in range(6):
			if A[j][i] == '1':
				b[j] = '0'
				cols += 1

# Account for the two extra columns used in the outside block
cols += 2

# Always select blocks incident in first six rows
for i in intersecting_blocks:
	b[i] = '1'

# If only three blocks incident to the special line then select those blocks
if num_used_blocks(b) == 3:
	print ''.join(b)+'1', cols, num_used_blocks(b)
	quit()

# If more than three blocks selected then find one of them to drop

for i in range(6):
	for i2 in range(6, 43):
		for j in range(19):
			for j2 in firstcols:
				if A[i][j]=='1' and A[i][j2]=='1' and A[i2][j]=='1':
					A[i2][j2] = '0'

rowcounts = [0 for i in range(43)]
for i in range(43):
	for j in range(6):
		if b[j] == '0':
			continue
		k = firstcols[j]
		if A[i][k] == ' ':
			rowcounts[i] += 1

counts = [0 for i in range(6)]
for i in range(43):
	for j in range(6):
		k = firstcols[j]
		if A[i][k] == ' ':
			counts[j] += rowcounts[i]

# Always select blocks that intersect in first 6 rows
while block_order[0] in intersecting_blocks:
	counts = counts[1:]
	block_order = block_order[1:]
	firstcols = firstcols[1:]

numblocks = num_used_blocks(b)

# Drop one block
orig_num_used_blocks = num_used_blocks(b)
while orig_num_used_blocks == num_used_blocks(b):
	for i in range(len(counts)):
		if counts[i] == min(counts):
			b[block_order[i]] = '0'
			counts.pop(i)
			block_order.pop(i)
			firstcols.pop(i)
			break

print ''.join(b)+'1', cols, numblocks
quit()
