import numpy as np
import math, sys, os.path, glob
from subprocess32 import call
from fractions import gcd

#sums of squares decompositions for 4*n for n = 1..69
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

if len(sys.argv) < 2:
	print "need order of search to run"
	quit()

n = int(sys.argv[1])

factors = [1]

inname = "input/squaredecomp/%s.in"
assumname = "input/squaredecomp/%s.in"
resultname = "results/squaredecomp/%s.out"
logname = "output/squaredecomp/%s.log"
archivename = "input/squaredecomp/%s.7z"

def runstr(n, c, k):
	if k == -1 and c == -1:
		return "%d" % n
	elif k == -1 and c == "*":
		return "%d.*" % n
	elif k == -1:
		return "%d.%d" % (n, c)
	elif k == "*" and c == "*":
		return "%d.*.*" % n
	elif k == "*":
		return "%d.%d.*" % (n, c)
	else:
		return "%d.%d.%d" % (n, c, k)
		#return ("%d.%d.%0" + numdigits + "d") % (n, c, k)

if not os.path.exists("input"):
        call(["mkdir", "input"])
if not os.path.exists("input/squaredecomp"):
	call(["mkdir", "input/squaredecomp"])

if not os.path.exists("output"):
        call(["mkdir", "output"])
if not os.path.exists("output/squaredecomp"):
	call(["mkdir", "output/squaredecomp"])

if not os.path.exists("results"):
        call(["mkdir", "results"])
if not os.path.exists("results/squaredecomp"):
	call(["mkdir", "results/squaredecomp"])

f = open(inname % runstr(n, -1, -1), "w")
#dependency on this file; inital set of constraints calculated.
call(["python", "hadamard_williamson_circ_SAT_binary_adder_squares_all.py", str(n)], stdout=f)
f.close()
f = open(inname % runstr(n, -1, -1), "r")
origlines = f.readlines()
f.close()
#call(["rm", inname % runstr(n, -1, -1), "r"])
origvars = int(origlines[0].split(" ")[-2])
orignumclauses = int(origlines[0].split(" ")[-1])

coprime_to_n = []
for l in range(n):
	if gcd(l, n) == 1:
		coprime_to_n.append(l)

def equivalent_reordering(X, k):
	n = len(X)
	assert(gcd(k, n) == 1)
	new = list(X)
	for i in range(n):
		new[(k*i)%n] = X[i]
	return new

numfactors = len(factors)

for c in range(len(sq[n])):

	sums = sq[n][c]
	indices = [0*(n/2+1)+1, 1*(n/2+1)+1, 2*(n/2+1)+1, 3*(n/2+1)+1]

	Alist = [[] for i in range(numfactors)]
	Blist = [[] for i in range(numfactors)]
	Clist = [[] for i in range(numfactors)]
	Dlist = [[] for i in range(numfactors)]

	for case in range(numfactors):
		# We consider the two cases with the two prime divisors being
		# swapped respectively
		count = 0
		p, q = factors[case], n/factors[case]
		pos = [[] for i in range(4)]
		psds = [[] for i in range(4)]
		X = [0 for i in range(p)] #temporary placeholder for a sequence of size p
		symlen = int(math.ceil((p+1)/2.0))
		XPSD = [0 for i in range(symlen)] #psds of X
		assert(n == p*q)
		#storing the positions of the first entry of each matrix in
		#the final Hadamard matrix (first line)

		upperlimit = (q+1)**symlen #total number of
		#sequences of lengths (p+1)/2 whose entries are odd and have
		#maximal value q. (without the odd condition
		#the base would be 2*q+1)
		for i in range(upperlimit):
			rowsum = 0
			for j in range(p):
				#brute force: all
				#possibilities from
				#[-q,...,-q] to
				#[q,...,q], stepping by for each coordinate.
				if j < symlen:
					t = int(i / (q+1)**j) % (q+1)
					X[j] = 2*(t-q)+q
				else:
					X[j] = X[p-j]

				rowsum += X[j]

			PSD_too_large = False

			DFT = np.fft.rfft(X)
			for l in range(symlen):
				XPSD[l] = (DFT[l].conj()*DFT[l]).real
				if XPSD[l] > 4*n+0.1:
					PSD_too_large = True

			if PSD_too_large == True:
				#print "PSD too large"
				continue

			for k in range(4):
				#we need to compute pos[k] specifically.
				if (rowsum != sums[k] and (sums[k] % 4) != 3) or (rowsum != -sums[k] and (sums[k] % 4) == 3):
				#if rowsum != sums[k]:
					continue
				pos[k].append(list(X))
				psds[k].append(list(XPSD))

		lenA = len(pos[0])
		lenB = len(pos[1])
		lenC = len(pos[2])
		lenD = len(pos[3])
		upperlimit = lenA*lenB*lenC*lenD
		print "%d-compressed sequences generated for case %s: %d A, %d B, %d C, %d D [%d total combinations]" % (q, sums, lenA, lenB, lenC, lenD, upperlimit)

		for ai in range(lenA):
			A = pos[0][ai]
			PSDSUMA = psds[0][ai]
			for bi in range(lenB):
				B = pos[1][bi]
				PSDSUMB = [sum(x) for x in zip(PSDSUMA, psds[1][bi])]
				if max(PSDSUMB) > 4*n+0.1:
					#print "PSD_A+PSD_B greater than 4*n"
					continue
				for ci in range(lenC):
					C = pos[2][ci]
					PSDSUMC = [sum(x) for x in zip(PSDSUMB, psds[2][ci])]
					if max(PSDSUMC) > 4*n+0.1:
						#print "PSD_A+PSD_B+PSD_C greater than 4*n"
						continue
					for di in range(lenD):
						D = pos[3][di]
						PSDSUMD = [sum(x) for x in zip(PSDSUMC, psds[3][di])]
						if max(PSDSUMD) > 4*n+0.1 or min(PSDSUMD) < 4*n-0.1:
							#print "PSD_A+PSD_B+PSD_C+PSD_D not 4*n"
							continue

						has_equiv = False

						if case == numfactors-1:
							for l in coprime_to_n:
								eqvA = equivalent_reordering(A, l)
								eqvB = equivalent_reordering(B, l)
								eqvC = equivalent_reordering(C, l)
								eqvD = equivalent_reordering(D, l)
								for x in range(len(Alist[case])):
									if eqvA == Alist[case][x] and eqvB == Blist[case][x] and eqvC == Clist[case][x] and eqvD == Dlist[case][x]:
										has_equiv = True
										break
							if has_equiv == True:
								break
							
						if has_equiv == True:
							print A, B, C, D, "is equivalent to a previous compressed quadruple"
							continue

						Alist[case].append(A)
						Blist[case].append(B)
						Clist[case].append(C)
						Dlist[case].append(D)
						count += 1
						print count, A, B, C, D

			print "%d/%d solved" % (ai+1, lenA)
			#if count > 10:
			#	break

	case1len = len(Alist[0])
	case2len = len(Alist[1]) if numfactors > 1 else 1
	case3len = len(Alist[2]) if numfactors > 2 else 1
	case4len = len(Alist[3]) if numfactors > 3 else 1

	print "Generating %d instances..." % (case1len*case2len*case3len*case4len)

	vars = origvars
	clauses = []
	clauses2 = []

	for l in range(4):
		varnum = sq[n][c][l]
		S = [[] for s in range(int(math.log(n,2))+1)]
		for k in range(n/2+1):
			index = k if k<=n/2 else n-k

			if k == 0 or (n % 2 == 0 and k == n/2):
				#if n % 2 == 0:
				S[0].append(indices[l]+index)
			else:
				S[1].append(indices[l]+index)

		while len(filter(lambda s: len(s)>1,S))>0:
			vars, clauses = do_add(S,vars,clauses)

		if (varnum % 4) != 3:
			sumnum = (n+varnum)/2
		else:
			sumnum = (n-varnum)/2

		for j in range(len(S)):
			if len(S[j]) == 0:
				continue
			assert(len(S[j])==1)

			if (sumnum & (2**j)) == 0:
				clauses2.append("%d" % -S[j][0])
			else:
				clauses2.append("%d" % S[j][0])

	# Add clauses based on the identity a[0]*b[0]*c[0]*d[0] = -a[i]*b[i]*c[i]*d[i] for odd n
	if n % 2 == 1:
		for j in range(1,n/2+1):
			clauses.append("%d %d %d %d 0" % (-(indices[0]+j), -(indices[1]+j), -(indices[2]+j), -(indices[3]+j)))
			clauses.append("%d %d %d %d 0" % (-(indices[0]+j), -(indices[1]+j), (indices[2]+j), (indices[3]+j)))
			clauses.append("%d %d %d %d 0" % (-(indices[0]+j), (indices[1]+j), -(indices[2]+j), (indices[3]+j)))
			clauses.append("%d %d %d %d 0" % (-(indices[0]+j), (indices[1]+j), (indices[2]+j), -(indices[3]+j)))
			clauses.append("%d %d %d %d 0" % ((indices[0]+j), -(indices[1]+j), -(indices[2]+j), (indices[3]+j)))
			clauses.append("%d %d %d %d 0" % ((indices[0]+j), -(indices[1]+j), (indices[2]+j), -(indices[3]+j)))
			clauses.append("%d %d %d %d 0" % ((indices[0]+j), (indices[1]+j), -(indices[2]+j), -(indices[3]+j)))
			clauses.append("%d %d %d %d 0" % ((indices[0]+j), (indices[1]+j), (indices[2]+j), (indices[3]+j)))

	origvars2 = vars
	origclauses = clauses
	origclauses2 = clauses2

	count = 0
	for case1 in range(case1len):
		for case2 in range(case2len):
			for case3 in range(case3len):
				for case4 in range(case4len):
					vars = origvars2
					clauses = list(origclauses)
					clauses2 = list(origclauses2)

					for case in range(numfactors):
						A = Alist[case][case1 if case == 0 else (case2 if case == 1 else (case3 if case == 2 else (case4 if case == 3 else -1)))]
						B = Blist[case][case1 if case == 0 else (case2 if case == 1 else (case3 if case == 2 else (case4 if case == 3 else -1)))]
						C = Clist[case][case1 if case == 0 else (case2 if case == 1 else (case3 if case == 2 else (case4 if case == 3 else -1)))]
						D = Dlist[case][case1 if case == 0 else (case2 if case == 1 else (case3 if case == 2 else (case4 if case == 3 else -1)))]
						p, q = factors[case], n/factors[case]

						for i in range(p):
							#Converting +-1 to 0,1
							numA = (q+A[i])/2
							numB = (q+B[i])/2
							numC = (q+C[i])/2
							numD = (q+D[i])/2
							assert(numA >= 0 and numA <= q)
							assert(numB >= 0 and numB <= q)
							assert(numC >= 0 and numC <= q)
							assert(numD >= 0 and numD <= q)

							for k in range(4):
								varstr = ("a" if k == 0 else ("b" if k == 1 else ("c" if k == 2 else ("d" if k == 3 else -1))))
								varnum = (numA if k == 0 else (numB if k == 1 else (numC if k == 2 else (numD if k == 3 else -1))))
						
								S = [[] for s in range(int(math.log(q,2))+1)]
								for j in range(q):
									index = (i+p*j if i+p*j <= n/2 else n-(i+p*j))
									#if j != 0:
									#	print "+",
									#print "%s%d (%d)" % (varstr, i+p*j, indices[k]+index),
									S[0].append(indices[k]+index)
								#print "= %d" % varnum

								assert(len(S[0])==q)

								while len(filter(lambda s: len(s)>1,S))>0:
									vars, clauses = do_add(S,vars,clauses)

								for j in range(len(S)):
									if len(S[j]) == 0:
										continue
									assert(len(S[j])==1)

									if (varnum & (2**j)) == 0:
										clauses2.append("%d" % -S[j][0])
									else:
										clauses2.append("%d" % S[j][0])

					count += 1
					f = open(assumname % runstr(n,c,-1), "w")
					f.write("p cnf %d %d\n" % (vars, orignumclauses+len(clauses)+len(clauses2)))
					for line in origlines[1:]:
						f.write(line)
					for cl in clauses:
						f.write(cl+"\n")
					for cl in clauses2:
						f.write(cl+" 0\n")
					f.close()

files = glob.glob(assumname % runstr(n,"*",-1))

if files == []:
	print "No instances generated!"
else:
	print "Archiving %d instances..." % len(files)
	f = open("out", "w")
	call(["zip", archivename % runstr(n,-1,-1)] + files, stdout=f)
	f.close()
	#for i in range(1,count+1):
	#	f = open(logname % runstr(n,c,i), "w")
	#	call(["./rlglucose", inname % runstr(n,c,i), resultname % runstr(n,c,i)])
	#	f.close()
