#!/bin/bash

# Script to verify that any solutions of the main instances (partial solutions of a projective plane incidence matrix) do not extend to all six blocks and an outside block

# Ensure that results are read from and output to main directory
if [ ${PWD##*/} == "final-step" ]
then
	# Make main directory the working directory
	cd ..
fi

ALLCASES=(1 2 3 5 6 7 8 9 11 12 13 15 16 17 18 20 21 22 23 24 25 26 27 33 34 36 37 39 41 42 43 46 47 48 49 50 51 53 55 56 58 60 63 65 66)

if [ -z $1 ]
then
	echo "Need case # of the case to solve (or 'all') once all partial solutions of the selected blocks have been recorded"
	exit
fi

if [ "$1" == "all" ]
then
	range=${ALLCASES[*]}
elif [ $1 -ge 1 ] 2>/dev/null && [ $1 -le 66 ]
then
	range=$1
else
	echo "Case needs to be between 1 and 66"
	exit
fi

# Check if directory a2s already exists
if [ ! -d a2s ]
then
	# Copy the A2 enumeration results into a2s directory if they have already been computed
	if [ -d ../a2/a2s ]
	then
		mkdir a2s
		cp ../a2/a2s/* a2s
	else
		# Download precomputed A2s if the A2 enumeration results do not exist
		echo "A2 results are missing; downloading a list of precomputed A2s"
		git clone https://github.com:curtisbright/a2s.git
	fi
elif [ ! -f a2s/$case.complete ]
then
	if [ -f ../a2/a2s/$case.complete ]
	then
		cp ../a2/a2s/$case.complete a2s
	else
		echo "Case $case A2s need to be computed first"
		exit
	fi
fi

# Compile MapleSAT and DRAT-trim
if [ ! -f maplesat_static ] || [ ! -f drat-trim ]
then
	./compile.sh
fi

# Create directories to hold instances and output
mkdir -p a2clauses
mkdir -p cnf
mkdir -p final-cnf
mkdir -p proof
mkdir -p log

allblocks="1111111"
maxcol_min=60

# Solve specified cases
for case in $range
do
	# Check if any partial solutions were found in this case
	if ls recorded/$case/$case.*.recorded 1> /dev/null 2> /dev/null
	then
		# Create directories to hold instances and output
		mkdir -p a2clauses/$case
		mkdir -p cnf/$case
		mkdir -p final-cnf/$case
		mkdir -p proof/$case
		mkdir -p log/$case

		# Determine how many columns to use in the final SAT instance (minimum # columns used in the previous instances)
		for f in recorded/$case/$case.*.recorded
		do
			maxcol=`echo $f | cut -d'.' -f2 | cut -d'-' -f2`
			maxcol_min=$(( $maxcol < $maxcol_min ? $maxcol : $maxcol_min ))
		done

		# Generate incremental set of assumptions and SAT instance
		echo "Generating list of assumptions and SAT instance to use in case $case..."
		make final-cnf/$case/$case.assums
		make final-cnf/$case/$case.$allblocks-$maxcol_min.final-cnf

		# Solve the incremental SAT instance using the generated assumptions
		command="./maplesat_static -no-pre -assumptions=final-cnf/$case/$case.assums final-cnf/$case/$case.$allblocks-$maxcol_min.final-cnf proof/$case/$case.$allblocks-$maxcol_min.proof | tee log/$case/$case.$allblocks-$maxcol_min.solve"
		echo $command
		eval $command

		# Add the negation of each set of assumptions to the end of the DRAT proof in order to have DRAT-trim verify they have been proved
		sed -e 's/ / -/g' -e 's/-0/0/' -e 's/a //' final-cnf/$case/$case.assums >> proof/$case/$case.$allblocks-$maxcol_min.proof

		# Use DRAT-trim in forward mode to verify that the negation of each set of assumptions (appended to the generated proof) have been proven
		command="./drat-trim final-cnf/$case/$case.$allblocks-$maxcol_min.final-cnf proof/$case/$case.$allblocks-$maxcol_min.proof -f > log/$case/$case.$allblocks-$maxcol_min.verify"
		echo $command
		eval $command

		# Check that all lemmas are verified; since this is an incremental SAT instance the proof will not end with the empty clause
		if grep "all lemmas verified" log/$case/$case.$allblocks-$maxcol_min.verify -q
		then
			echo "c all lemmas verified"
		fi
	else
		echo "No recorded partial solutions of the selected blocks were found in case $case"
	fi
done
