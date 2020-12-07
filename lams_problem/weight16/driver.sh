#!/bin/bash
mkdir -p cnf
mkdir -p exhaust
mkdir -p assums
mkdir -p cubes
mkdir -p log
mkdir -p out

genproof=false

set -o pipefail

if [ -z $1 ]
then
	echo "Need case to run (1a, 1b, 1c, 2, 3, 4, 5, 6a, 6b, 6c)"
	exit
elif [ $1 == "1a" ] || [ $1 == "1b" ] || [ $1 == "1c" ]
then
	# Use block symmetry breaking method in cases 1a-c
	./block_driver.sh $1 $2 $3
	exit
fi

if [ ! -s maplesat_static ]
then
	./compile_maplesat.sh
fi

if [ ! -s march_cu ] || [ ! -s lingeling ] || ( $genproof && [ ! -s drat-trim ] )
then
	./compile_tools.sh
fi

case=$1

# Automatic selection of cubing bound based on case
if [ $case == "2" ]
then
	b=7100	# 8121 free vars
elif [ $case == "3" ]
then
	b=2750	# 3561 free vars
elif [ $case == "4" ]
then
	b=1925	# 2486 free vars
elif [ $case == "5" ]
then
	b=1500	# 1952 free vars
elif [ $case == "6a" ]
then
	b=1300	# 1731 free vars
elif [ $case == "6b" ]
then
	b=1050	# 1465 free vars
elif [ $case == "6c" ]
then
	b=1050	# 1493 free vars
fi

if [ ! -z $2 ]
then
	b=$2	# Custom cubing bound
fi

# Generate SAT instance
if [ ! -s cnf/$case.lex.cnf ]
then
	python projplane_sat_lex.py $case > cnf/$case.lex.cnf
fi

# Simplify SAT instance
if [ ! -s cnf/$case.lex.simp.cnf ]
then
	simpcommand="./lingeling cnf/$case.lex.cnf -q -s -O5 -o cnf/$case.lex.simp.cnf -t out/$case.lex.simp.out | tee log/$case.lex.simp"
	echo $simpcommand
	eval $simpcommand
fi

# Generate cubes
if [ ! -s cubes/$case.$b.lex.simp.cubes ]
then
	cubecommand="./march_cu cnf/$case.lex.simp.cnf -n $b -o cubes/$case.$b.lex.simp.cubes | tee log/$case.$b.lex.simp.cube"
	echo $cubecommand
	eval $cubecommand
fi

# Solve SAT instance using cube-and-conquer
if [ ! -s out/$case.$b.lex.simp.out ]
then
	if $genproof
	then
		proofout="out/$case.$b.lex.simp.out "
	fi
	solvecommand="./maplesat_static -assumptions=cubes/$case.$b.lex.simp.cubes cnf/$case.lex.simp.cnf -verb=0 -reduce-frac=10 -print-bound=10 $proofout| tee log/$case.$b.lex.pre.solve"
	echo $solvecommand
	eval $solvecommand
	result=$?
else
	result=20
fi

# Verify proof if generated
if $genproof && [ $result -eq 20 ]
then
	cat out/$case.lex.simp.out out/$case.$b.lex.simp.out > out/$case.$b.lex.simp.all.out
	checkcommand="./drat-trim cnf/$case.lex.cnf out/$case.$b.lex.simp.all.out -C -b -l out/$case.$b.lex.simp.trim.out | tee log/$case.$b.lex.pre.simp"
	echo $checkcommand
	eval $checkcommand
	result=$?

	# Compress proof in 7z archive
	if [ $result -eq 0 ]
	then
		compresscommand="7z a out/$case.$b.lex.simp.trim.out.7z $PWD/out/$case.$b.lex.simp.trim.out | tee log/$case.$b.lex.pre.compress"
		echo $compresscommand
		eval $compresscommand
		result=$?

		# Remove uncompressed proof if archiving succeeded
		if [ $result -eq 0 ]
		then
			rm out/$case.$b.lex.simp.out out/$case.$b.lex.simp.trim.out out/$case.$b.lex.simp.all.out
		fi
	fi
fi
