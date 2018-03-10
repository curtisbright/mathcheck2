import numpy as np
import math, sys, os.path, glob
from subprocess32 import call
from fractions import gcd
from mathcheck_common import sq, do_add

if len(sys.argv) < 2:
	print "need order (or min and max order) of search to run (an optionally, a specific case those orders)"
	quit()

verbose = False

n1 = int(sys.argv[1])
if len(sys.argv) > 2:
	n2 = int(sys.argv[2])
else:
	n2 = n1

inname = "input/comp/%s.in"
assumname = "input/comp/%s.assum"
archivename = "archives/comp/%s.zip"
compname = "input/comp/%s.comp"

if not os.path.exists("input"): call(["mkdir", "input"])
if not os.path.exists("input/comp"): call(["mkdir", "input/comp"])
if not os.path.exists("archives"): call(["mkdir", "archives"])
if not os.path.exists("archives/comp"): call(["mkdir", "archives/comp"])

def runstr(n, c, k):
	if k == -1 and c == -1:
		return "%d" % n
	elif k == -1:
		return "%d.%d" % (n, c)
	elif k == "*" and c == "*":
		return "%d.*.*" % n
	elif k == "*":
		return "%d.%d.*" % (n, c)
	else:
		return "%d.%d.%d" % (n, c, k)
		#return ("%d.%d.%0" + numdigits + "d") % (n, c, k)

for n in range(n1, n2+1):
	if n == 9:
		factors = [3]
	elif n == 15:
		factors = [3, 5]
	elif n == 21:
		factors = [3, 7]
	elif n == 25:
		factors = [5]
	elif n == 27:
		factors = [3, 9]
	elif n == 33:
		factors = [3, 11]
	elif n == 35:
		factors = [5, 7]
	elif n == 39:
		factors = [3, 13]
	elif n == 45:
		factors = [3, 5]
	elif n == 49:
		factors = [7]
	elif n == 51:
		factors = [3, 17]
	elif n == 55:
		factors = [5, 11]
	elif n == 57:
		factors = [3, 19]
	elif n == 63:
		factors = [3, 7]
	elif n == 65:
		factors = [5]
	elif n == 69:
		factors = [3, 23]
	elif n % 2 == 0:
		factors = [n/2]
	else:
		factors = [n]

	numfactors = len(factors)

	f = open(inname % runstr(n, -1, -1), "w")
	#dependency on this file; inital set of constraints calculated.
	call(["python", "hadamard_williamson_circ_SAT_binary_adder_squares_all.py", str(n)], stdout=f)
	f.close()

	f = open(inname % runstr(n, -1, -1), "r")
	origlines = f.readlines()
	f.close()

	vars = int(origlines[0].split(" ")[-2])
	orignumclauses = int(origlines[0].split(" ")[-1])

	squaredecomp_binary_adder_vars = [[] for i in range(4)]
	compression1_binary_adder_vars = [[[] for j in range(factors[0])] for i in range(4)]
	if numfactors > 1:
		compression2_binary_adder_vars = [[[] for j in range(factors[1])] for i in range(4)]

	indices = [0*(n/2+1)+1, 1*(n/2+1)+1, 2*(n/2+1)+1, 3*(n/2+1)+1]
	clauses = []
	instancescount = 0

	for c in range(4):
		squaredecomp_binary_adder_vars[c] = [[] for s in range(int(math.log(n,2))+1)]
		for k in range(n/2+1):
			index = k if k<=n/2 else n-k

			if k == 0 or (n % 2 == 0 and k == n/2):
				squaredecomp_binary_adder_vars[c][0].append(indices[c]+index)
			else:
				squaredecomp_binary_adder_vars[c][1].append(indices[c]+index)

		while len(filter(lambda s: len(s)>1,squaredecomp_binary_adder_vars[c]))>0:
			vars, clauses = do_add(squaredecomp_binary_adder_vars[c],vars,clauses)

		if verbose:
			for j in range(len(squaredecomp_binary_adder_vars[c])):
				if len(squaredecomp_binary_adder_vars[c][j]) > 0:
					assert(len(squaredecomp_binary_adder_vars[c][j])==1)
					print "var %d is the %dth bit of rowsum(%c)" % (squaredecomp_binary_adder_vars[c][j][0], j, chr(65+c))

		p, q = factors[0], n/factors[0]

		for i in range(p):
			compression1_binary_adder_vars[c][i] = [[] for s in range(int(math.log(q,2))+1)]
			for j in range(q):
				index = (i+p*j if i+p*j <= n/2 else n-(i+p*j))
				compression1_binary_adder_vars[c][i][0].append(indices[c]+index)

			assert(len(compression1_binary_adder_vars[c][i][0])==q)

			while len(filter(lambda s: len(s)>1,compression1_binary_adder_vars[c][i]))>0:
				vars, clauses = do_add(compression1_binary_adder_vars[c][i],vars,clauses)

		if verbose:
			for i in range(p):
				for j in range(len(compression1_binary_adder_vars[c][i])):
					if len(compression1_binary_adder_vars[c][i][j]) > 0:
						assert(len(compression1_binary_adder_vars[c][i][j])==1)
						print "var %d is the %dth bit of compression1(%c)[%d]" % (compression1_binary_adder_vars[c][i][j][0], j, chr(65+c), i)

		if numfactors > 1:
			p, q = factors[1], n/factors[1]

			for i in range(p):
				compression2_binary_adder_vars[c][i] = [[] for s in range(int(math.log(q,2))+1)]
				for j in range(q):
					index = (i+p*j if i+p*j <= n/2 else n-(i+p*j))
					compression2_binary_adder_vars[c][i][0].append(indices[c]+index)

				assert(len(compression2_binary_adder_vars[c][i][0])==q)

				while len(filter(lambda s: len(s)>1,compression2_binary_adder_vars[c][i]))>0:
					vars, clauses = do_add(compression2_binary_adder_vars[c][i],vars,clauses)
			if verbose:
				for i in range(p):
					for j in range(len(compression2_binary_adder_vars[c][i])):
						if len(compression2_binary_adder_vars[c][i][j]) > 0:
							assert(len(compression2_binary_adder_vars[c][i][j])==1)
							print "var %d is the %dth bit of compression2(%c)[%d]" % (compression2_binary_adder_vars[c][i][j][0], j, chr(65+c), i)

	# Add clauses based on the identity a[0]*b[0]*c[0]*d[0] = -a[i]*b[i]*c[i]*d[i]
	#   as well as the the first bit of the matrices A, B, C, D (for odd n)
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

		if ((1+n)/2) % 2 == 0:
			clauses.append("%d 0" % -indices[0])
			clauses.append("%d 0" % -indices[1])
			clauses.append("%d 0" % -indices[2])
			clauses.append("%d 0" % -indices[3])
		else:
			clauses.append("%d 0" % indices[0])
			clauses.append("%d 0" % indices[1])
			clauses.append("%d 0" % indices[2])
			clauses.append("%d 0" % indices[3])

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

	def generate_assumptions(c, p, q, A, B, C, D, assumptions):
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
				varnum = (numA if k == 0 else (numB if k == 1 else (numC if k == 2 else (numD if k == 3 else -1))))
				if c == 0:
					S = compression1_binary_adder_vars[k][i]
				else:
					S = compression2_binary_adder_vars[k][i]
				for j in range(len(S)):
					if len(S[j]) == 0:
						continue
					assert(len(S[j])==1)

					if (varnum & (2**j)) == 0:
						assumptions.append("%d" % -S[j][0])
					else:
						assumptions.append("%d" % S[j][0])

	def generate_neg_clause(c, k, p, q, X):
		newclause = ""
		for i in range(p):
			#Converting +-1 to 0,1
			numX = (q+X[i])/2
			assert(numX >= 0 and numX <= q)

			varnum = numX
			if c == 0:
				S = compression1_binary_adder_vars[k][i]
			else:
				S = compression2_binary_adder_vars[k][i]
			for j in range(len(S)):
				if len(S[j]) == 0:
					continue
				assert(len(S[j])==1)

				if (varnum & (2**j)) == 0:
					newclause += ("%d " % S[j][0])
				else:
					newclause += ("%d " % -S[j][0])

		newclause += "0"
		return newclause

	# Generate base instance without filtering clauses
	f = open(inname % runstr(n, -1, -1), "w")
	f.write("p cnf %d %d\n" % (vars, orignumclauses+len(clauses)))
	for line in origlines[1:]:
		f.write(line)
	for cl in clauses:
		f.write(cl+"\n")

	origclauses = list(clauses)

	cases_to_generate = range(len(sq[n]))
	if len(sys.argv) > 3:
		assert(int(sys.argv[3]) in cases_to_generate)
		cases_to_generate = [int(sys.argv[3])]

	for c in cases_to_generate:

		clauses = list(origclauses)
		sums = sq[n][c]
		toolarge = [[] for i in range(4)]

		p, q = n, 1
		X = [0 for i in range(p)] #temporary placeholder for a sequence of size p
		symlen = int(math.ceil((p+1)/2.0))
		#storing the positions of the first entry of each matrix in
		#the final Hadamard matrix (first line)

		upperlimit = (q+1)**symlen #total number of
		#sequences of lengths (p+1)/2 whose entries are odd and have
		#maximal value q. (without the odd condition
		#the base would be 2*q+1)
		for i in range(upperlimit):
			if i > 0 and i % 1000 == 0:
				print "%d/%d complete (%d %d %d %d filtered)" % (i, upperlimit, len(toolarge[0]), len(toolarge[1]), len(toolarge[2]), len(toolarge[3]))
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
				if (DFT[l].conj()*DFT[l]).real > 4*n+0.1:
					PSD_too_large = True

			if PSD_too_large == True:
				for k in range(4):
					if (rowsum != sums[k] and (sums[k] % 4) != 3) or (rowsum != -sums[k] and (sums[k] % 4) == 3):
						pass
					else:
						toolarge[k].append(list(X))

		print "%d/%d complete (%d %d %d %d filtered)" % (upperlimit, upperlimit, len(toolarge[0]), len(toolarge[1]), len(toolarge[2]), len(toolarge[3]))

		for l in range(4):
			for x in toolarge[l]:
				clause_to_add = ""
				for i in range(int(math.ceil((n+1)/2.0))):
					clause_to_add = clause_to_add + ("%d " % (-(i+indices[l])*x[i]))
				clause_to_add = clause_to_add + "0"
				clauses.append(clause_to_add)

		Alist = [[] for i in range(numfactors)]
		Blist = [[] for i in range(numfactors)]
		Clist = [[] for i in range(numfactors)]
		Dlist = [[] for i in range(numfactors)]

		toolargecase = [[[] for i in range(4)] for j in range(numfactors)]

		for case in range(numfactors):
			# We consider the two cases with the two prime divisors being
			# swapped respectively
			instancescount = 0
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
				if i > 0 and i % 1000 == 0:
					print "%d/%d complete (%d %d %d %d filtered)" % (i, upperlimit, len(toolargecase[case][0]), len(toolargecase[case][1]), len(toolargecase[case][2]), len(toolargecase[case][3]))
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
					for k in range(4):
						if (rowsum != sums[k] and (sums[k] % 4) != 3) or (rowsum != -sums[k] and (sums[k] % 4) == 3):
							pass
						else:
							toolargecase[case][k].append(list(X))

				for k in range(4):
					#we need to compute pos[k] specifically.
					if (rowsum != sums[k] and (sums[k] % 4) != 3) or (rowsum != -sums[k] and (sums[k] % 4) == 3):
					#if rowsum != sums[k]:
						continue
					pos[k].append(list(X))
					psds[k].append(list(XPSD))

			print "%d/%d complete (%d %d %d %d filtered)" % (i, upperlimit, len(toolargecase[case][0]), len(toolargecase[case][1]), len(toolargecase[case][2]), len(toolargecase[case][3]))

			for k in range(4):
				for X in toolargecase[case][k]:
					clauses.append(generate_neg_clause(case, k, p, q, X))
					print case, k, p, q, X, generate_neg_clause(case, k, p, q, X)

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
								#print A, B, C, D, "is equivalent to a previous compressed quadruple"
								continue

							Alist[case].append(A)
							Blist[case].append(B)
							Clist[case].append(C)
							Dlist[case].append(D)
							instancescount += 1
							print instancescount, A, B, C, D

							if case == numfactors-1:

								instances_to_generate = 1 if numfactors == 1 else len(Alist[0])

								for case1 in range(instances_to_generate):
									f = open(compname % runstr(n, c, instancescount), "w")
									if numfactors > 1:
										f.write("%d " % (n/factors[case]))
										for x in Alist[0][case1]:
											f.write("%d " % x)
										for x in Blist[0][case1]:
											f.write("%d " % x)
										for x in Clist[0][case1]:
											f.write("%d " % x)
										for x in Dlist[0][case1]:
											f.write("%d " % x)
										f.write("\n")
									f.write("%d " % (factors[case]))
									for x in A:
										f.write("%d " % x)
									for x in B:
										f.write("%d " % x)
									for x in C:
										f.write("%d " % x)
									for x in D:
										f.write("%d " % x)
									f.write("\n")
									f.close()

									assumptions = []

									for l in range(4):
										varnum = sq[n][c][l]

										if (varnum % 4) != 3:
											sumnum = (n+varnum)/2
										else:
											sumnum = (n-varnum)/2

										S = squaredecomp_binary_adder_vars[l]
										for j in range(len(S)):
											if len(S[j]) == 0:
												continue
											assert(len(S[j])==1)

											if (sumnum & (2**j)) == 0:
												assumptions.append("%d" % -S[j][0])
											else:
												assumptions.append("%d" % S[j][0])

									if numfactors > 1:
										generate_assumptions(0, factors[0], n/factors[0], Alist[0][case1], Blist[0][case1], Clist[0][case1], Dlist[0][case1], assumptions)

									generate_assumptions(0 if numfactors == 1 else 1, p, q, A, B, C, D, assumptions)

									f = open(assumname % runstr(n,c,instancescount), "w")
									for cl in assumptions:
										f.write(cl+"\n")
									f.close()

				print "%d/%d solved" % (ai+1, lenA)

		f = open(inname % runstr(n, c, -1), "w")
		f.write("p cnf %d %d\n" % (vars, orignumclauses+len(clauses)))
		for line in origlines[1:]:
			f.write(line)
		for cl in clauses:
			f.write(cl+"\n")

	files = glob.glob(assumname % runstr(n,"*","*"))
	compfiles = glob.glob(compname % runstr(n,"*","*"))

	if files == []:
		print "No instances generated!"
	else:
		print "Archiving %d instances..." % len(files)
		f = open("out", "w")
		call(["zip", archivename % runstr(n,-1,-1), inname % runstr(n,-1,-1)] + files + compfiles, stdout=f)
		f.close()
