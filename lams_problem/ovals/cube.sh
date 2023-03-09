#!/bin/bash
l=$1

if [ -z $1 ]
then
	echo "Need case #"
	exit
fi

if [ ! -f cnf/b1-5.$l.simp.cnf ]
then
	./simp.sh $l
fi

# Generate list of cubes for SAT instance
command="./march_cu cnf/b1-5.$l.simp.cnf -o cubes/b1-5.$l.simp.cubes -n 684"

echo $command
eval $command

