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

printalign(10, "case")
#printalign(1, "&")
printalign(10, "gen comps")
#printalign(1, "&")
printalign(10, "gen pairs")
#printalign(1, "&")
printalign(10, "sort")
#printalign(1, "&")
printalign(10, "join")
#printalign(1, "&")
printalign(10, "remequiv")
#printalign(1, "&")
printalign(10, "solve")
#printalign(1, "&")
printalign(10, "tally")
#printalign(1, "&")
printalign(10, "TOTAL (h)")
#printalign(1, "&")
printalign(10, "numinsts")
#printalign(1, "&")
printalign(10, "numsols")
#printalign(1, "\\\\")
print ""

totalgentime = 0

if n1 % 2 == 0:
	orderdiff = 2
else:
	orderdiff = 6

for n in range(n1, n2+1, orderdiff):
	if n%2 == 0:
		d = 2
	elif n%3 == 0:
		d = 3
	elif n%5 == 0:
		d = 5
	elif n%7 == 0:
		d = 7
	else:
		d = 1
	l = n/d

	cases = range(4)
	totaltime = 0
	gentime = 0
	gencomptime = 0
	genpairtime = 0
	sorttime = 0
	jointime = 0
	equivpairstime = 0
	solvetime = 0
	equivexhausttime = 0
	numinsts = 0
	numsols = 0

	if os.path.exists("timings/{0}.{1}.gencomptime".format(n, l)):
		f = open("timings/{0}.{1}.gencomptime".format(n, l), "r")
		lines = f.readlines()
		f.close()
		if len(lines)>0:
			gentime += float(lines[0])

	totalgentime += gentime

	for c in cases:

		if os.path.exists("timings/{0}.{1}.{2}.genpairtime".format(n, c, l)):
			f = open("timings/{0}.{1}.{2}.genpairtime".format(n, c, l), "r")
			lines = f.readlines()
			f.close()
			if len(lines)>0:
				genpairtime += float(lines[0])

		if os.path.exists("timings/{0}.{1}.{2}.AB.sorttime".format(n, c, l)):
			f = open("timings/{0}.{1}.{2}.AB.sorttime".format(n, c, l), "r")
			lines = f.readlines()
			f.close()
			if len(lines)>0:
				sorttime += float(lines[0])

		if os.path.exists("timings/{0}.{1}.{2}.CD.sorttime".format(n, c, l)):
			f = open("timings/{0}.{1}.{2}.CD.sorttime".format(n, c, l), "r")
			lines = f.readlines()
			f.close()
			if len(lines)>0:
				sorttime += float(lines[0])

		if os.path.exists("timings/{0}.{1}.{2}.0.jointime".format(n, c, l)):
			for s in range(10):
				f = open("timings/{0}.{1}.{2}.{3}.jointime".format(n, c, l, s), "r")
				lines = f.readlines()
				f.close()
				if len(lines)>0:
					jointime += float(lines[0])
		elif os.path.exists("timings/{0}.{1}.{2}.jointime".format(n, c, l)):
			f = open("timings/{0}.{1}.{2}.jointime".format(n, c, l), "r")
			lines = f.readlines()
			f.close()
			if len(lines)>0:
				jointime += float(lines[0])

		if os.path.exists("timings/{0}.{1}.equivpairstime".format(n, c, l)):
			f = open("timings/{0}.{1}.equivpairstime".format(n, c, l), "r")
			lines = f.readlines()
			f.close()
			if len(lines)>0:
				equivpairstime += float(lines[0])

		if os.path.exists("timings/{0}.{1}.solvetimesum".format(n, c)):
			f = open("timings/{0}.{1}.solvetimesum".format(n, c), "r")
			lines = f.readlines()
			f.close()
			if len(lines)>0:
				solvetime += float(lines[0])
		elif os.path.exists("timings/{0}.{1}.solvetime".format(n, c)):
			f = open("timings/{0}.{1}.solvetime".format(n, c), "r")
			lines = f.readlines()
			f.close()
			if len(lines)>0:
				solvetime += float(lines[0])

		if os.path.exists("matchedseqns/{0}.{1}.{2}.inequiv".format(n, c, l)):
			f = open("matchedseqns/{0}.{1}.{2}.inequiv".format(n, c, l), "r")
			numinsts += len(f.readlines())
			f.close()

	if os.path.exists("timings/{0}.equivexhausttime".format(n)):
		f = open("timings/{0}.equivexhausttime".format(n), "r")
		lines = f.readlines()
		f.close()
		if len(lines)>0:
			equivexhausttime += float(lines[0])

	if os.path.exists("exhaust/{0}.inequiv".format(n)):
		f = open("exhaust/{0}.inequiv".format(n), "r")
		numsols += len(f.readlines())
		f.close()

	totaltime += gentime 
	totaltime += genpairtime
	totaltime += sorttime
	totaltime += jointime
	totaltime += equivpairstime
	totaltime += solvetime
	totaltime += equivexhausttime

	printalign(10, n)
	#printalign(1, "&")
	printalign(10, gentime)
	#printalign(1, "&")
	printalign(10, genpairtime)
	#printalign(1, "&")
	printalign(10, sorttime)
	#printalign(1, "&")
	printalign(10, jointime)
	#printalign(1, "&")
	printalign(10, equivpairstime)
	#printalign(1, "&")
	printalign(10, solvetime)
	#printalign(1, "&")
	printalign(10, equivexhausttime)
	#printalign(1, "&")
	printalign(10, totaltime/float(60*60))
	#printalign(1, "&")
	printalign(10, numinsts)
	#printalign(1, "&")
	printalign(10, numsols)
	#printalign(1, "\\\\")
	print ""

#print "Total gen time: {0}".format(totalgentime)
