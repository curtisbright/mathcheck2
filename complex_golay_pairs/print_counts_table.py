import sys
import os.path

if len(sys.argv) < 2:
	print "need order (or min and max order) of timings to print"
	quit()

n1 = int(sys.argv[1])
if len(sys.argv) > 2:
	n2 = int(sys.argv[2])
else:
	n2 = n1

def printalign(w, s):
	if isinstance(s, float):
		print str("%.2f" % s) + " "*(w-len(str("%.2f" % s))),
	else:
		print str(s) + " "*(w-len(str(s))),

printalign(10, "n")
printalign(10, "# seqs")
printalign(10, "# total")
printalign(10, "# inequiv")
print ""

totalgentime = 0

for n in range(max(n1, 2), n2+1):
	numseqs = 0
	numtotal = 0
	numinequiv = 0

	if os.path.exists("enumeration/{0}.all".format(n)):
		f = open("enumeration/{0}.all".format(n), "r")
		numtotal += len(f.readlines())
		f.close()

	if os.path.exists("enumeration/{0}.inequiv".format(n)):
		f = open("enumeration/{0}.inequiv".format(n), "r")
		numinequiv += len(f.readlines())
		f.close()

	if os.path.exists("enumeration/{0}.seqs".format(n)):
		f = open("enumeration/{0}.seqs".format(n), "r")
		numseqs += len(f.readlines())
		f.close()

	printalign(10, n)
	#printalign(1, "&")
	printalign(10, numseqs)
	#printalign(1, "&")
	printalign(10, numtotal)
	#printalign(1, "&")
	printalign(10, numinequiv)
	#printalign(2, "\\\\")
	print ""

