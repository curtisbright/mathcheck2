#!/bin/bash
l=$1

if [ -z $1 ]
then
	echo "Need case #"
	exit
fi

if [ -f out/b1-5.$l.simp.with.units.trim.out ]
then
	# Compress proof
	command="7z a proof/b1-5.$l.7z $PWD/out/b1-5.$l.simp.with.units.trim.out"

	echo $command
	eval $command
	result=$?

	# Delete uncompressed proofs
	if [ $result -eq 0 ]
	then
		command="rm out/b1-5.$l.simp.with.units.out out/b1-5.$l.simp.with.units.trim.out"
		echo $command
		eval $command
	fi
fi
