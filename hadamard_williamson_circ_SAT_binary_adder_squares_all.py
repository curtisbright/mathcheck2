##################################################
# DESCRIPTION:
##################################################
# This script takes an input parameter n in NN and prints to the
# standard output a SAT-instance in DIMACS form, which corresponds
# to finding three circulant matrices A,B,C and D in {-1,1}^{n x n},
# that are commuting, symmetric and fulfill the formula
# A^2 + B^2 + C^2 + D^2 = 4nI_n
# The respective entries are represented by the first 4*(n/2+1) variables,
# i.e. variables 1 ... n/2+1 belong to A
#      variables n/2+2 ... n+4 belong to B
#      variables n+4 ... 3n/2 + 3 belong to C
#  and variables 3n/2 + 3 ... 2n+4 belong to D.
# (reminder: A,B,C and D are assumed to be circulant and symmetric,
# i.e. they are each completely determined by n/2 + 1 variables and
# can afterwards be completed by a script.) The other variables
# are only placeholders used to check the conditions on A,B,C and D.
# In this script, we obtain the other conditions by using binary adders.

##################################################
# SEE ALSO
##################################################
# hadamard_williamson_circ_SAT_merge_sort.py

##################################################
# LICENSE:
##################################################
# Copyright (C) 2015  Curtis Bright, Albert Heinle and Saeed Nejati

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

##################################################
# IMPORT
##################################################
import sys
from math import log, floor
##################################################

# SAT search for Williamson matrices (used to construct Hadamard matrices);
# version with minimal number of variables introduced

sq = [0 for i in range(70)]
sq[1] = [[1, 1, 1, 1]]
sq[2] = [[0, 0, 2, 2]]
sq[3] = [[1, 1, 1, 3]]
sq[4] = [[0, 0, 0, 4], [2, 2, 2, 2]]
sq[5] = [[1, 1, 3, 3]]
sq[6] = [[0, 2, 2, 4]]
sq[7] = [[1, 1, 1, 5], [1, 3, 3, 3]]
sq[8] = [[0, 0, 4, 4]]
sq[9] = [[1, 1, 3, 5], [3, 3, 3, 3]]
sq[10] = [[0, 0, 2, 6], [2, 2, 4, 4]]
sq[11] = [[1, 3, 3, 5]]
sq[12] = [[0, 4, 4, 4], [2, 2, 2, 6]]
sq[13] = [[1, 1, 1, 7], [1, 1, 5, 5], [3, 3, 3, 5]]
sq[14] = [[0, 2, 4, 6]]
sq[15] = [[1, 1, 3, 7], [1, 3, 5, 5]]
sq[16] = [[0, 0, 0, 8], [4, 4, 4, 4]]
sq[17] = [[1, 3, 3, 7], [3, 3, 5, 5]]
sq[18] = [[0, 0, 6, 6], [0, 2, 2, 8], [2, 4, 4, 6]]
sq[19] = [[1, 1, 5, 7], [1, 5, 5, 5], [3, 3, 3, 7]]
sq[20] = [[0, 0, 4, 8], [2, 2, 6, 6]]
sq[21] = [[1, 1, 1, 9], [1, 3, 5, 7], [3, 5, 5, 5]]
sq[22] = [[0, 4, 6, 6], [2, 2, 4, 8]]
sq[23] = [[1, 1, 3, 9], [3, 3, 5, 7]]
sq[24] = [[0, 4, 4, 8]]
sq[25] = [[1, 1, 7, 7], [1, 3, 3, 9], [1, 5, 5, 7], [5, 5, 5, 5]]
sq[26] = [[0, 0, 2, 10], [0, 2, 6, 8], [4, 4, 6, 6]]
sq[27] = [[1, 1, 5, 9], [1, 3, 7, 7], [3, 3, 3, 9], [3, 5, 5, 7]]
sq[28] = [[2, 2, 2, 10], [2, 6, 6, 6], [4, 4, 4, 8]]
sq[29] = [[1, 3, 5, 9], [3, 3, 7, 7]]
sq[30] = [[0, 2, 4, 10], [2, 4, 6, 8]]
sq[31] = [[1, 1, 1, 11], [1, 5, 7, 7], [3, 3, 5, 9], [5, 5, 5, 7]]
sq[32] = [[0, 0, 8, 8]]
sq[33] = [[1, 1, 3, 11], [1, 1, 7, 9], [1, 5, 5, 9], [3, 5, 7, 7]]
sq[34] = [[0, 0, 6, 10], [0, 6, 6, 8], [2, 2, 8, 8], [2, 4, 4, 10]]
sq[35] = [[1, 3, 3, 11], [1, 3, 7, 9], [3, 5, 5, 9]]
sq[36] = [[0, 0, 0, 12], [0, 4, 8, 8], [2, 2, 6, 10], [6, 6, 6, 6]]
sq[37] = [[1, 1, 5, 11], [1, 7, 7, 7], [3, 3, 3, 11], [3, 3, 7, 9], [5, 5, 7, 7]]
sq[38] = [[0, 2, 2, 12], [0, 4, 6, 10], [4, 6, 6, 8]]
sq[39] = [[1, 3, 5, 11], [1, 5, 7, 9], [3, 7, 7, 7], [5, 5, 5, 9]]
sq[40] = [[0, 0, 4, 12], [4, 4, 8, 8]]
sq[41] = [[1, 1, 9, 9], [3, 3, 5, 11], [3, 5, 7, 9]]
sq[42] = [[0, 2, 8, 10], [2, 2, 4, 12], [2, 6, 8, 8], [4, 4, 6, 10]]
sq[43] = [[1, 1, 1, 13], [1, 1, 7, 11], [1, 3, 9, 9], [1, 5, 5, 11], [5, 7, 7, 7]]
sq[44] = [[0, 4, 4, 12], [2, 6, 6, 10]]
sq[45] = [[1, 1, 3, 13], [1, 3, 7, 11], [1, 7, 7, 9], [3, 3, 9, 9], [3, 5, 5, 11], [5, 5, 7, 9]]
sq[46] = [[0, 2, 6, 12], [2, 4, 8, 10]]
sq[47] = [[1, 3, 3, 13], [1, 5, 9, 9], [3, 3, 7, 11], [3, 7, 7, 9]]
sq[48] = [[0, 8, 8, 8], [4, 4, 4, 12]]
sq[49] = [[1, 1, 5, 13], [1, 5, 7, 11], [3, 3, 3, 13], [3, 5, 9, 9], [5, 5, 5, 11], [7, 7, 7, 7]]
sq[50] = [[0, 0, 2, 14], [0, 0, 10, 10], [0, 6, 8, 10], [2, 4, 6, 12], [6, 6, 8, 8]]
sq[51] = [[1, 1, 9, 11], [1, 3, 5, 13], [3, 5, 7, 11], [5, 7, 7, 9]]
sq[52] = [[0, 0, 8, 12], [2, 2, 2, 14], [2, 2, 10, 10], [4, 8, 8, 8], [6, 6, 6, 10]]
sq[53] = [[1, 3, 9, 11], [1, 7, 9, 9], [3, 3, 5, 13], [5, 5, 9, 9]]
sq[54] = [[0, 2, 4, 14], [0, 4, 10, 10], [0, 6, 6, 12], [2, 2, 8, 12], [4, 6, 8, 10]]
sq[55] = [[1, 1, 7, 13], [1, 5, 5, 13], [1, 7, 7, 11], [3, 3, 9, 11], [3, 7, 9, 9], [5, 5, 7, 11]]
sq[56] = [[0, 4, 8, 12]]
sq[57] = [[1, 1, 1, 15], [1, 3, 7, 13], [1, 5, 9, 11], [3, 5, 5, 13], [3, 7, 7, 11], [7, 7, 7, 9]]
sq[58] = [[0, 0, 6, 14], [2, 4, 4, 14], [2, 8, 8, 10], [4, 4, 10, 10], [4, 6, 6, 12]]
sq[59] = [[1, 1, 3, 15], [3, 3, 7, 13], [3, 5, 9, 11], [5, 7, 9, 9]]
sq[60] = [[2, 2, 6, 14], [2, 6, 10, 10], [4, 4, 8, 12]]
sq[61] = [[1, 1, 11, 11], [1, 3, 3, 15], [1, 5, 7, 13], [1, 9, 9, 9], [5, 5, 5, 13], [5, 7, 7, 11]]
sq[62] = [[0, 2, 10, 12], [0, 4, 6, 14], [2, 6, 8, 12]]
sq[63] = [[1, 1, 5, 15], [1, 1, 9, 13], [1, 3, 11, 11], [1, 7, 9, 11], [3, 3, 3, 15], [3, 5, 7, 13], [3, 9, 9, 9], [5, 5, 9, 11]]
sq[64] = [[0, 0, 0, 16], [8, 8, 8, 8]]
sq[65] = [[1, 3, 5, 15], [1, 3, 9, 13], [3, 3, 11, 11], [3, 7, 9, 11], [7, 7, 9, 9]]
sq[66] = [[0, 2, 2, 16], [0, 2, 8, 14], [0, 8, 10, 10], [2, 4, 10, 12], [4, 4, 6, 14], [6, 8, 8, 10]]
sq[67] = [[1, 5, 11, 11], [1, 7, 7, 13], [3, 3, 5, 15], [3, 3, 9, 13], [5, 5, 7, 13], [5, 9, 9, 9], [7, 7, 7, 11]]
sq[68] = [[0, 0, 4, 16], [0, 8, 8, 12], [2, 6, 6, 14], [6, 6, 10, 10]]
sq[69] = [[1, 1, 7, 15], [1, 5, 5, 15], [1, 5, 9, 13], [3, 5, 11, 11], [3, 7, 7, 13], [5, 7, 9, 11]]

# Do one bitwise addition (using either a full or half adder) to the leftmost
# entry of S which is not fully simplified yet
def do_add(S,vars, clauses):
    for i in range(len(S)):
		s = S[i]
		# 3-bit adder
		if len(s) >= 3:
			# Three bits to add together
			x1 = s.pop()
			x2 = s.pop()
			x3 = s.pop()

			clauses.append("-%d %d -%d -%d 0" % (x1, x2, x3, vars+2))
			clauses.append("-%d -%d %d -%d 0" % (x1, x2, x3, vars+2))
			clauses.append("%d %d -%d %d 0" % (x1, x2, x3, vars+2))
			clauses.append("%d -%d %d %d 0" % (x1, x2, x3, vars+2))
			clauses.append("%d -%d -%d 0" % (x1, vars+1, vars+2))
			clauses.append("-%d %d %d 0" % (x1, vars+1, vars+2))
			clauses.append("%d %d -%d 0" % (x2, x3, vars+1))
			clauses.append("-%d -%d %d 0" % (x2, x3, vars+1))
			clauses.append("%d %d %d -%d 0" % (x1, x2, x3, vars+2))
			clauses.append("-%d -%d -%d %d 0" % (x1, x2, x3, vars+2))

			S[i].append(vars+2)
			S[i+1].append(vars+1)
			vars += 2

			return (vars, clauses)
		# 2-bit adder
		if len(s) >= 2:
			# Two bits to add together
			x1 = s.pop()
			x2 = s.pop()

			clauses.append("%d -%d 0" % (x2, vars+1))
			clauses.append("-%d -%d %d 0" % (x1, x2, vars+1))
			clauses.append("%d -%d %d 0" % (x1, x2, vars+2))
			clauses.append("-%d %d %d 0" % (x1, x2, vars+2))
			clauses.append("-%d -%d 0" % (vars+1, vars+2))
			clauses.append("%d %d -%d 0" % (x1, x2, vars+2))

			S[i].append(vars+2)
			S[i+1].append(vars+1)
			vars += 2
			return (vars, clauses)

    return (vars,clauses)

def create_vars_and_clauses(n):
  # Count number of variables introduced so far
  vars = 0
  # Clauses introduced so far
  clauses = []
  # Variables for entries of matrices A, B, C, D
  A = [[0 for j in range(n/2+1)] for k in range(4)]
  # Create 1 variable for each entry of the matrix
  for k in range(4):
  	for j in range(n/2+1):
  		vars += 1
  		A[k][j] = vars
  # Variables for component-wise products
  C = [[[0 for j in range(n)] for k in range(n)] for l in range(4)]

  # Dictonary to store variables which are duplicates
  dupes = {}
  const_var = 0

  # Create 1 variable for each entry of each component-wise product
  for l in range(4):
	for j in range(n):
		for k in range(n):
			index1 = k if k<=n/2 else n-k
			index2 = ((j+k) % n) if ((j+k) % n) <= n/2 else n-((j+k) % n)
			x = A[l][index1]
			y = A[l][index2]
			x, y = min(x,y), max(x,y)

			if x == y:
				if const_var != 0:
					C[l][j][k] = const_var
				else:
					vars += 1
					C[l][j][k] = vars
					const_var = vars

					# newvar = 1
					clauses.append("%d 0" % vars)
			else:
				if (x,y) in dupes:
					C[l][j][k] = dupes[(x,y)]
				else:
					vars += 1
					C[l][j][k] = vars
					dupes[(x,y)] = vars

					# newvar = x XNOR y
					clauses.append("%d %d %d 0" % (vars, -x, -y))
					clauses.append("%d %d %d 0" % (vars, x, y))
					clauses.append("%d %d %d 0" % (-vars, x, -y))
					clauses.append("%d %d %d 0" % (-vars, -x, y))

  # For each component-wise product we will sum together the number of high bits
  # (i.e., compute the hamming weight of the component-wise product)
  for j in range(1,n/2+1):
	# The variables in S[k] are considered to have weight 2^k in the sum
	S = [[] for k in range(2+n+int(log(n, 2)))]

	tmpS = []

	# Give all entries of the component-wise product between rows i and j a weight of 1
	for l in range(4):
		for k in range(n):
			tmpS.append(C[l][j][k])

	# remove one copy of each element which occurs twice
	tmpS = sorted(tmpS)[::2]

	num_const_var = tmpS.count(const_var)
	while tmpS.count(const_var) > 0:
		tmpS.remove(const_var)

	# handle elements which occur more than once efficiently
	for x in tmpS:
		if not(x in S[0] or x in S[1] or x in S[2]):
			if tmpS.count(x) == 1:
				S[0].append(x)
			elif tmpS.count(x) == 2:
				S[1].append(x)
			elif tmpS.count(x) == 3:
				S[0].append(x)
				S[1].append(x)
			elif tmpS.count(x) == 4:
				S[2].append(x)
			else:
				print x, tmpS.count(x)
				assert(False)

	# Keep adding together variables which have the same weight until there exists
	# exactly one variable of each weight (which gives us the binary representation
	# of the hamming weight)
	while len(filter(lambda s: len(s)>1,S))>0:#not(sum_simplified(S)):
		#print S
		vars, clauses = do_add(S,vars,clauses)

	# Add a clause to ensure that the final sum represents exactly n in binary
	for k in range(len(S)):
		if len(S[k]) >= 1:
			if ((n-num_const_var) & (2**k)) == 0:
				clauses.append("%d 0" % -S[k][0])
			else:
				clauses.append("%d 0" % S[k][0])

  return (vars,clauses)
        
if __name__=='__main__':
  # The order of the Hadamard matrix to search for
  n = int(sys.argv[1])

  try:
    if n<2:
      raise Exception()
  except:
    print "This script needs to be called with an integer argument, indicating \
the size of the respective A, B, C, D matrices. I.e.:\n\
python %s n\n\
where n>1 is an integer."%sys.argv[0]
    sys.exit(-1)
  vars, clauses = create_vars_and_clauses(n)
  # Output clauses in DIMACS format
  print "p cnf %d %d" % (vars, len(clauses))
  for c in clauses:
  	print c
