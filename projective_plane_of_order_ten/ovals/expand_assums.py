import sys

# Script to expand a list of assumptions to a set of unit clauses

if len(sys.argv) <= 2:
	print "Need file and line # in file containing the assumptions"
	exit()

# File that contains the assumptions to use
fstr = sys.argv[1]

# Line of the file that contains the assumptions to use
l = int(sys.argv[2])

f = open(fstr, "r")

line = f.readlines()[l][2:-1]
for x in line.split(" ")[:-1]:
	print "{0} 0".format(x)
f.close()

