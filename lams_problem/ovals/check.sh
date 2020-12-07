#!/bin/bash
l=$1

if [ -z $1 ]
then
	echo "Need case #"
	exit
fi

if [ -f out/b1-5.$l.simp.with.units.out ] && [ "$(tail out/b1-5.$l.simp.with.units.out -n 1)" == "0" ]
then
	# Verify proof
	command="./drat-trim cnf/b1-5.$l.simp.with.units.cnf out/b1-5.$l.simp.with.units.out -C -b -l out/b1-5.$l.simp.with.units.trim.out"

	echo $command
	eval $command
	result=$?
else
	result=1
fi

exit $result
