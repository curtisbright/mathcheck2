#!/bin/bash

# Script for attempting to extend all completions of blocks 1-5 to blocks 1-6 (zero-based numbering)

if [ ! -f cnf/b1-6.cnf ]
then
	python2 projplane_sat.py 1 6 > cnf/b1-6.cnf
fi

cat exhaust/b1-5.*.exhaust > exhaust/b1-5.all

if [ -s exhaust/b1-5.all ]
then
	command="./maplesat_static -no-pre -assumptions=exhaust/b1-5.all cnf/b1-6.cnf out/b1-6.out -verb=0"

	echo $command
	eval $command
fi
