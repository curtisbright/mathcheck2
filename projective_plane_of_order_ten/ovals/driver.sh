#!/bin/bash
mkdir -p cnf
mkdir -p out
mkdir -p cubes
mkdir -p proof
mkdir -p log
mkdir -p exhaust

if [ -z $1 ]
then
	echo "Need case # to solve (or first and last case #s to solve in a range).  Valid case #s are from 0 to 395 inclusive."
	exit
fi

if [ -z $2 ]
then
	range=$1
elif [ $1 -ge $2 ]
then
	range=`seq $1 -1 $2`
else
	range=`seq $1 $2`
fi

if [ ! -f ../march_cu ] || [ ! -f ../lingeling ] || [ ! -f ../drat-trim ] || [ ! -f ../maplesat_static ]
then
	./compile_tools.sh
fi

set -o pipefail

for n in $range
do
	if [ ! -f cnf/b1-5.$n.simp.cnf ]
	then
		command="./simp.sh $n | tee log/$n.simp.log"
		echo $command
		eval $command
	fi

	if [ ! -f cubes/b1-5.$n.simp.cubes ]
	then
		command="./cube.sh $n | tee log/$n.cube.log"
		echo $command
		eval $command
	fi

	if [ ! -f out/b1-5.$n.simp.with.units.out ] || [ "$(tail out/b1-5.$n.simp.with.units.out -n 1)" != "0" ]
	then
		if [ -f out/b1-5.$n.simp.with.units.out ]
		then
			rm out/b1-5.$n.simp.with.units.out
		fi
		command="./conquer.sh $n | tee log/$n.solve.log"
		echo $command
		eval $command
	fi

	result=0
	if [ ! -f out/b1-5.$n.simp.with.units.trim.out ]
	then
		command="./check.sh $n | tee log/$n.check.log"
		echo $command
		eval $command
		result=$?
	fi

	if [ -f out/b1-5.$n.simp.with.units.trim.out ] && [ $result -eq 0 ]
	then
		command="./compress.sh $n | tee log/$n.compress.log"
		echo $command
		eval $command
	fi
done

