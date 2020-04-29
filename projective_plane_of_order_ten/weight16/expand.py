# Expand a line of assumptions into a list of unit clauses

import sys

if len(sys.argv) <= 1:
	print "Need the name of the file containing the assumptions to expand"
	quit()

# If -commas given as a parameter then expand as a comma-separated string
use_commas = ("-commas" in sys.argv)
if "-commas" in sys.argv:
	sys.argv.remove("-commas")

filename = sys.argv[1]
# If second parameter l given then expand the l'th assumption line
l = int(sys.argv[2]) if len(sys.argv) >= 3 else 0
# If third parameter skip given then expand the skip'th line immediately following the l'th assumption line (ignoring the sign of the literals)
skip = int(sys.argv[3]) if len(sys.argv) >= 4 else 0

f = open(filename, "r")

st = ""

count = 0

lines = f.readlines()

for line in lines:
	if "a" in line:
		if count==l:
			if skip > 0:
				count += 1
				continue
			line = line[2:-1]
			for x in line.split(" ")[:-1]:
				st += "{0},".format(x)
				if not use_commas:
					print "{0} 0".format(x)
			break
		count += 1
		continue
	if skip > 0:
		if count==l+skip:
			line = line[:-1]
			for x in line.split(" ")[:-1]:
				st += "{0},".format(abs(int(x)))
				if not use_commas:
					print "{0} 0".format(abs(int(x)))
			break
		if count > l:
			count += 1

if use_commas:
	print st[:-1]

f.close()
