#!/bin/bash
l=$1

if [ -z $1 ]
then
	echo "Need case #"
	exit
fi

# Generate SAT instance for blocks 1-5 (zero-based numbering)
if [ ! -f cnf/b1-5.cnf ]
then
	python2 projplane_sat.py 1 5 > cnf/b1-5.cnf
fi

# Generate assumptions specifying the 1-factorization with given case #
if [ ! -f cnf/$l.assums ]
then
	python2 expand_assums.py k10_1-factorizations $l > cnf/$l.assums
fi

# Generate SAT instance for blocks 1-5 with block 1 defined by the 1-factorization with given case #
if [ ! -f cnf/b1-5.$l.cnf ]
then
	cat cnf/b1-5.cnf cnf/$l.assums > cnf/b1-5.$l.cnf
	numclauses=$(wc -l < cnf/b1-5.$l.cnf)
	numclauses=$((numclauses-1))
	sed -i -E "s/p cnf ([0-9]*) ([0-9]*)/p cnf \1 $numclauses/" cnf/b1-5.$l.cnf
fi

# Simplify SAT instance using Lingeling preprocessor
command="./lingeling -q -O5 -s cnf/b1-5.$l.cnf -o cnf/b1-5.$l.simp.cnf -t proof/b1-5.$l.proof"

echo $command
eval $command

