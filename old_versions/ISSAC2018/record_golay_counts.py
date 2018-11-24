import sys
import time
import os.path
from subprocess32 import call

verbose = False
printdecomps = False
printtable = False

if len(sys.argv) == 1:
	print "Need order (or min and max orders) of complex Golay pairs to count"
	quit()

n1 = int(sys.argv[1])
n2 = int(sys.argv[2]) if len(sys.argv) > 2 else n1

if not os.path.exists("timings"): call("mkdir timings".split(" "))
if not os.path.exists("enumeration"): call("mkdir enumeration".split(" "))

def const_mult(s):
	r = ""
	for c in s:
		if c == '+':
			r += 'i'
		elif c == 'i':
			r += '-'
		elif c == '-':
			r += 'j'
		else:
			r += '+'
	return r
	
def pos_mult(s):
	r = ""
	count = 0
	for c in s:
		if count == 0:
			r += c
		elif count == 1:
			if c == '+':
				r += 'i'
			elif c == 'i':
				r += '-'
			elif c == '-':
				r += 'j'
			else:
				r += '+'
		elif count == 2:
			if c == '+':
				r += '-'
			elif c == 'i':
				r += 'j'
			elif c == '-':
				r += '+'
			else:
				r += 'i'
		elif count == 3:
			if c == '+':
				r += 'j'
			elif c == 'i':
				r += '+'
			elif c == '-':
				r += 'i'
			else:
				r += '-'
		count = (count+1)%4
	return r

def conjugate_reverse(s):
	r = ""
	for c in s:
		if c == 'i':
			r = 'j' + r
		elif c == 'j':
			r = 'i' + r
		else:
			r = c + r
	return r
	
def reverse(s):
	r = ""
	for c in s:
		r = c + r
	return r

def E1(G):
	X = G[0]
	Y = G[1]
	return (reverse(X), reverse(Y))
	
def E2(G):
	X = G[0]
	Y = G[1]
	return (conjugate_reverse(X), Y)
	
def E3(G):
	X = G[0]
	Y = G[1]
	return (Y, X)
	
def E4(G):
	X = G[0]
	Y = G[1]
	return (const_mult(X), Y)
	
def E5(G):
	X = G[0]
	Y = G[1]
	return (pos_mult(X), pos_mult(Y))

for n in range(n1, n2+1):
	start = time.time()
	all_golay_pairs = set()
	all_golay_seqs = set()

	f = open("pairs/pairs.{0}.txt".format(n))
	lines = f.readlines()
	f.close()

	finequiv = open("enumeration/{0}.inequiv".format(n), "w")

	count = 0
	for line in lines:
		new_golay_pairs = set()
		new_golay_pairs_list = list()
		parts = line.split(" ")
		A = parts[0]
		B = parts[1][:-1]
		G = (A, B)
		if not G in all_golay_pairs:
			count += 1
			finequiv.write(line)
			new_golay_pairs.add(G)
			new_golay_pairs_list.append(G)
			
			i = 0
			while i < len(new_golay_pairs_list):
				g = new_golay_pairs_list[i]
				g1 = E1(g)
				g2 = E2(g)
				g3 = E3(g)
				g4 = E4(g)
				g5 = E5(g)
				if not g1 in new_golay_pairs:
					new_golay_pairs.add(g1)
					new_golay_pairs_list.append(g1)
				if not g2 in new_golay_pairs:
					new_golay_pairs.add(g2)
					new_golay_pairs_list.append(g2)
				if not g3 in new_golay_pairs:
					new_golay_pairs.add(g3)
					new_golay_pairs_list.append(g3)
				if not g4 in new_golay_pairs:
					new_golay_pairs.add(g4)
					new_golay_pairs_list.append(g4)
				if not g5 in new_golay_pairs:
					new_golay_pairs.add(g5)
					new_golay_pairs_list.append(g5)
				i += 1
			
			for g in new_golay_pairs:
				all_golay_pairs.add(g)
				all_golay_seqs.add(g[0])
				all_golay_seqs.add(g[1])

			if verbose:
				print G, "is equivalent to %d complex Golay pairs" % len(new_golay_pairs)
	
	print "Order %d: Sequences: %d, Total Pairs: %d, Inequiv Pairs: %d, Time: %.2f sec" % (n, len(all_golay_seqs), len(all_golay_pairs), count, time.time()-start)

	f = open("timings/{0}.record.time".format(n), "w")
	f.write("%.2f\n" % (time.time()-start))
	f.close()
	finequiv.close()

	fseqs = open("enumeration/{0}.seqs".format(n), "w")
	for g in all_golay_seqs:
		fseqs.write(g + "\n")
	fseqs.close()

	fall = open("enumeration/{0}.all".format(n), "w")
	for g in all_golay_pairs:
		fall.write(g[0] + " " + g[1] + "\n")
	fall.close()
