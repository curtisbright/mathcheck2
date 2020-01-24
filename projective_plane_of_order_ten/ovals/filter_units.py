import sys

# Script to print out all unit clauses from a SAT instance CNF file

if len(sys.argv) <= 1:
	print "Need CNF file"
	exit()

with open(sys.argv[1]) as f:
	lines = f.readlines()

for line in lines:
	if len(line.split(" "))==2:
		print line[:-1]
