#!/bin/bash

while getopts "t" opt
do
	case $opt in
		t) l=$2; toplevel=" -l2 $((397-l)) -o2 cubes/b1-5.$l.simp.toplevel" ;;
	esac
done
shift $((OPTIND-1))

if [ -z $1 ]
then
	echo "Need case # [run with -t as first argument to generate a collection of toplevel cubes]"
	exit
fi

l=$1

if [ ! -f cnf/b1-5.$l.simp.cnf ]
then
	./simp.sh $l
fi

# Generate list of cubes for SAT instance
command="./march_cu cnf/b1-5.$l.simp.cnf -o cubes/b1-5.$l.simp.cubes -n 684$toplevel"

echo $command
eval $command

