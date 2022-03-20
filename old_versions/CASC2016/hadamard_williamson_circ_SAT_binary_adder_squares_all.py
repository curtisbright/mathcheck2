##################################################
# DESCRIPTION:
##################################################
# This script takes an input parameter n in NN and prints to the
# standard output a SAT-instance in DIMACS form, which corresponds
# to finding three circulant matrices A, B, C and D in {-1,1}^{n x n},
# that are commuting, symmetric and fulfill the formula
# A^2 + B^2 + C^2 + D^2 = 4n*I_n
# The respective entries are represented by the first 4*(floor(n/2)+1) variables,
# i.e., variables                1 ...   floor(n/2) + 1 belong to A
#       variables   floor(n/2) + 2 ... 2*floor(n/2) + 2 belong to B
#       variables 2*floor(n/2) + 3 ... 3*floor(n/2) + 3 belong to C
#   and variables 3*floor(n/2) + 4 ... 4*floor(n/2) + 4 belong to D.
# (reminder: A, B, C and D are assumed to be circulant and symmetric,
# i.e., they are each completely determined by 4*(floor(n/2)+1) variables and
# can afterwards be completed by a script.) The other variables
# are only placeholders used to check the conditions on A, B, C and D.
# In this script, we obtain the other conditions by using binary adders.

#################################################
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
from mathcheck_common import sq, do_add
##################################################

# SAT search for Williamson matrices (used to construct Hadamard matrices);
# version with minimal number of variables introduced

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
python2 %s n\n\
where n>1 is an integer."%sys.argv[0]
    sys.exit(-1)
  vars, clauses = create_vars_and_clauses(n)
  # Output clauses in DIMACS format
  print "p cnf %d %d" % (vars, len(clauses))
  for c in clauses:
  	print c
