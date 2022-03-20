#!/bin/bash

# Create directories to hold instances and output
mkdir -p cnf
mkdir -p log
mkdir -p out
mkdir -p a2s

if [ -z $1 ]
then
	echo "Need case # of A2s to generate (or 'all')"
	exit
fi

# Get case # or range of cases to generate A2s for
if [ "$1" == "all" ]
then
	range=`seq 1 66`
elif [ $1 -ge 1 ] 2>/dev/null && [ $1 -le 66 ]
then
	range=$1
else
	echo "Case needs to be between 1 and 66"
	exit
fi

# Compile MapleSAT and GRATgen
if [ ! -f maplesat_static ] || [ ! -f gratgen ]
then
	./compile.sh
fi

# Solve A2 instances for all cases in given range
for case in $range
do
	# Generate A2 SAT instance for this case
	command="python2 satgen_a2.py $case > cnf/a2.$case.cnf"
	echo $command
	eval $command

	# Exhaustively solve A2 SAT instance using "recorded objects" symmetry breaking
	command="./maplesat_static cnf/a2.$case.cnf -complete=a2s/$case.complete -rejected=out/a2.$case.rejected -recorded=out/a2.$case.recorded out/a2.$case.proof | tee log/a2.$case.log"
	echo $command
	eval $command

	# Generate a SAT instance with blocking clauses for each possible solution of the original instance
	VARS=$(head -n 1 cnf/a2.$case.cnf | cut -d' ' -f3)
	LEN1=$(cat cnf/a2.$case.cnf | wc -l)
	LEN2=$(cat a2s/$case.complete | wc -l)
	LEN3=$(cat out/a2.$case.rejected | wc -l)

	echo "p cnf $VARS $((LEN1+LEN2+LEN3-1))" > cnf/a2.$case.check.cnf
	tail cnf/a2.$case.cnf -n +2 >> cnf/a2.$case.check.cnf
	sed -e 's/ / -/g' -e 's/-0/0/g' -e 's/a //g' a2s/$case.complete >> cnf/a2.$case.check.cnf
	sed -e 's/ / -/g' -e 's/-0/0/g' -e 's/a //g' out/a2.$case.rejected >> cnf/a2.$case.check.cnf

	# Verify that the instance with blocking clauses added is unsatisfiable
	command="./gratgen cnf/a2.$case.check.cnf out/a2.$case.proof 2> log/a2.$case.check"
	echo $command
	eval $command

	grep "VERIFIED" log/a2.$case.check

	# Verify that all rejected solutions are isomorphic to one of the recorded solutions
	command="python2 check.py $case | tee log/a2.$case.tracescheck"
	echo $command
	eval $command
done
