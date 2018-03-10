import sys, os.path
from subprocess32 import call
from mathcheck_common import sq

if len(sys.argv) < 2:
	print "need order (or min and max order) of cases to generate"
	quit()

n = int(sys.argv[1])

inname = "input/compstring/%d.in"

if not os.path.exists("input"): call(["mkdir", "input"])
if not os.path.exists("input/compstring"): call(["mkdir", "input/compstring"])

indices = [0*(n/2+1)+1, 1*(n/2+1)+1, 2*(n/2+1)+1, 3*(n/2+1)+1]
f = open(inname % n, "w")
if n%2 == 1:
	f.write("p cnf {0} {1}\n".format(4*(n/2)+4, 8*(n/2)+4))
	for j in range(1,n/2+1):
		#f.write("cx%d %d %d %d 0\n" % (-(indices[0]+j), (indices[1]+j), (indices[2]+j), (indices[3]+j)))
		f.write("%d %d %d %d 0\n" % (-(indices[0]+j), -(indices[1]+j), -(indices[2]+j), -(indices[3]+j)))
		f.write("%d %d %d %d 0\n" % (-(indices[0]+j), -(indices[1]+j), (indices[2]+j), (indices[3]+j)))
		f.write("%d %d %d %d 0\n" % (-(indices[0]+j), (indices[1]+j), -(indices[2]+j), (indices[3]+j)))
		f.write("%d %d %d %d 0\n" % (-(indices[0]+j), (indices[1]+j), (indices[2]+j), -(indices[3]+j)))
		f.write("%d %d %d %d 0\n" % ((indices[0]+j), -(indices[1]+j), -(indices[2]+j), (indices[3]+j)))
		f.write("%d %d %d %d 0\n" % ((indices[0]+j), -(indices[1]+j), (indices[2]+j), -(indices[3]+j)))
		f.write("%d %d %d %d 0\n" % ((indices[0]+j), (indices[1]+j), -(indices[2]+j), -(indices[3]+j)))
		f.write("%d %d %d %d 0\n" % ((indices[0]+j), (indices[1]+j), (indices[2]+j), (indices[3]+j)))

	if ((1+n)/2) % 2 == 0:
		f.write("%d 0\n" % -indices[0])
		f.write("%d 0\n" % -indices[1])
		f.write("%d 0\n" % -indices[2])
		f.write("%d 0\n" % -indices[3])
	else:
		f.write("%d 0\n" % indices[0])
		f.write("%d 0\n" % indices[1])
		f.write("%d 0\n" % indices[2])
		f.write("%d 0\n" % indices[3])
else:
	f.write("p cnf {0} 1\n".format(4*(n/2)+4))
	f.write("{0} -{0} 0\n".format(4*(n/2)+4))

f.close()
