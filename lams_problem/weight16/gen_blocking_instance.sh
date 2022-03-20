#!/bin/bash
mkdir -p cnf
mkdir -p exhaust
mkdir -p assums

# Weight 16 SAT generation script with block symmetry removal method

if [ -z $1 ]
then
	echo "Need case to run"
	exit
fi

case=$1

if [ ! -s maplesat_static_$case ]
then
	./compile_maplesat.sh
fi

if [ $case == "1b" ] || [ $case == "1c" ]
then
	cols=24
else
	cols=23
fi

# Generate weight 16 incidence constraints up to first block
if [ ! -s cnf/$case.$cols.cnf ]
then
	python2 projplane_sat.py $case $cols > cnf/$case.$cols.cnf
fi

# Exhaustively find all nonequivalent instances of first block and sort them by their automorphism group sizes
if [ ! -s exhaust/$case.$cols.exhaust ]
then
	command="./maplesat_static_$case -isoblock -no-pre cnf/$case.$cols.cnf -exhaustive=exhaust/$case.$cols.exhaust-withsizes -exhaustive2=exhaust/$case.$cols.exhaust-blocking -printassums -equivsizes"
	echo $command
	eval $command
	cut -c1-183 exhaust/$case.$cols.exhaust-withsizes > exhaust/$case.$cols.exhaust
	echo "Sorting the possible representatives of the first block by the size of their automorphism groups..."
	python2 sort_exhaust.py exhaust/$case.$cols.exhaust-withsizes exhaust/$case.$cols.exhaust exhaust/$case.$cols.exhaust-blocking
fi

# Generate weight 16 incidence constraints including all blocks
if [ ! -s cnf/$case.cnf ]
then
	python2 projplane_sat.py $case > cnf/$case.cnf
fi

# Generate block symmetry breaking method clauses
if [ ! -s exhaust/$case.$cols.exhaust-cnf ]
then
	echo "Generating a single SAT instance containing all the symmetry breaking clauses..."
	python2 gen_block_clauses_icnf.py $case
	python2 gen_block_clauses_cnf.py $case
fi

# Generate a single SAT instance containing all incidence constraints and block symmetry breaking clauses
if [ ! -s cnf/$case.blocking.combine.cnf ]
then
	cat cnf/$case.cnf exhaust/$case.$cols.exhaust-cnf.sorted > cnf/$case.blocking.combine.cnf
	numclauses=$(wc -l cnf/$case.blocking.combine.cnf | cut -d ' ' -f1)
	num=$(wc -l exhaust/$case.$cols.exhaust-cnf.sorted | cut -d ' ' -f1)
	sed -i -E "s/p cnf ([0-9]*) ([0-9]*)/p cnf $((8880+num)) $((numclauses-1))/" cnf/$case.blocking.combine.cnf
fi
