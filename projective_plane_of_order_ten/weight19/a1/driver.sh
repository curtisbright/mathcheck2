#!/bin/bash

# Compile MapleSAT and GRATgen
if [ ! -f maplesat_static ] || [ ! -f gratgen ]
then
	./compile.sh
fi

# Generate A1 SAT instance
command="python satgen_a1.py > a1.cnf"
echo $command
eval $command

# Exhaustively solve A1 SAT instance
command="./maplesat_static a1.cnf -no-pre -recorded=a1.recorded -rejected=a1.rejected a1.proof"
echo $command
eval $command

# Generate SAT instance with blocking clauses for each possible solution of the original instance
VARS=$(head -n 1 a1.cnf | cut -d' ' -f3)
LEN1=$(cat a1.cnf | wc -l)
LEN2=$(cat a1.recorded | wc -l)
LEN3=$(cat a1.rejected | wc -l)

echo "p cnf $VARS $((LEN1+LEN2+LEN3-1))" > a1.check.cnf
tail a1.cnf -n +2 >> a1.check.cnf
sed -e 's/ / -/g' -e 's/-0/0/g' -e 's/a //g' a1.recorded >> a1.check.cnf
sed -e 's/ / -/g' -e 's/-0/0/g' -e 's/a //g' a1.rejected >> a1.check.cnf

# Verify that instance with blocking clauses added is unsatisfiable
command="./gratgen a1.check.cnf a1.proof 2> a1.check.log"
echo $command
eval $command

grep "VERIFIED" a1.check.log

# Verify that all rejected solutions are isomorphic to one of the recorded solutions
command="python check.py"
echo $command
eval $command
