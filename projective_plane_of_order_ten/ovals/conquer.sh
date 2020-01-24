#!/bin/bash
l=$1
printbound=100

if [ -z $1 ]
then
	echo "Need case #"
	exit
fi

python filter_units.py cnf/b1-5.$l.cnf > cnf/b1-5.$l.units
cat cnf/b1-5.$l.simp.cnf cnf/b1-5.$l.units > cnf/b1-5.$l.simp.with.units.cnf

numclauses=$(wc -l < cnf/b1-5.$l.simp.with.units.cnf)
numclauses=$((numclauses-1))
sed -i -E "s/p cnf ([0-9]*) ([0-9]*)/p cnf \1 $numclauses/" cnf/b1-5.$l.simp.with.units.cnf

# Conquer SAT instance and generate DRAT proof and the satisfying completions (if any)
command="./maplesat_static -no-pre -assumptions=cubes/b1-5.$l.simp.cubes cnf/b1-5.$l.simp.with.units.cnf -verb=0 -print-bound=$printbound out/b1-5.$l.simp.with.units.out -exhaustive=exhaust/b1-5.$l.exhaust"

echo $command
eval $command

