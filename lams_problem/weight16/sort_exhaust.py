import sys

# Script to sort the possibilities for the first block by the size of their automorphism groups
# The 1st parameter should be the name of a file containing the automorphism group sizes (as the last # on each line)
# The 2nd parameter should be the name of a file containing the list of possibilities for the first block
# The 3rd parameter should be the name of a file containing the list of possibilities and clauses blocking all other equivalent possibilities

with open(sys.argv[1]) as f:
	lines = f.readlines()
	#lines.sort(key=lambda x : int(x.split(" ")[-1]), reverse=True)

with open(sys.argv[2]) as f2:
	lines2 = f2.readlines()

with open(sys.argv[3]) as g:
	glines = g.readlines()

newglines = []

curstr = ""

for line in glines:
	if "a" in line and curstr != "":
		newglines.append(curstr)
		curstr = line
	else:
		curstr += line

newglines.append(curstr)

newlist = []

for i in range(len(lines)):
	newlist.append([lines[i], lines2[i], newglines[i]])

newlist.sort(key=lambda x : int(x[0].split(" ")[-1]), reverse=True)

with open(sys.argv[1]+".sorted", "w") as f:
	with open(sys.argv[2]+".sorted", "w") as f2:
		with open(sys.argv[3]+".sorted", "w") as g:
			for i in range(len(newlist)):
				f.write(newlist[i][0])
				f2.write(newlist[i][1])
				g.write(newlist[i][2])
