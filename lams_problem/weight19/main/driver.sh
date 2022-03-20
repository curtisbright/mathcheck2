#!/bin/bash

# Driver script to solve the SAT instance associated with a given A1 case and A2 instance
# If the A2s have not already been enumerated using the A2 scripts then a list of precomputed A2s will be be downloaded

# Create directories to hold instances and output
mkdir -p base-cnf
mkdir -p a2clauses
mkdir -p cnf
mkdir -p simp-cnf
mkdir -p blocked-cnf
mkdir -p log
mkdir -p proof
mkdir -p cubes
mkdir -p recorded

if [ -z $2 ]
then
	echo "Need case # (as first parameter) and A2 instance # or 'all' (as second parameter) of the instances to generate and solve"
	exit
fi

if [ $1 -ge 1 ] 2>/dev/null && [ $1 -le 66 ]
then
	case=$1
else
	echo "Case # needs to be between 1 and 66"
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
		git clone https://github.com/curtisbright/a2s.git
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

numinstances=`cat a2s/$case.complete | wc -l`

if [ $numinstances -eq 0 ]
then
	echo "Case $case has no A2s to solve"
	exit
fi

if [ $case -eq 52 ]
then
	echo "Case $case may be eliminated by a theoretical argument (Lam, Crossfield, and Thiel 1985)"
	exit
fi

if [ $case -eq 32 ] || [ $case -eq 38 ] || [ $case -eq 54 ] || [ $case -eq 57 ] || [ $case -eq 64 ]
then
	echo "Case $case implies the existence of a word of weight 16 in the rowspace of A (Lam, Crossfield, and Thiel 1985)"
	exit
fi

if [ "$2" == "all" ]
then
	range=`seq 0 $((numinstances-1))`
elif [ $2 -ge 0 ] 2>/dev/null && [ $2 -lt $numinstances ]
then
	range=$2
else
	echo "Case $case instance # needs to be between 0 and $((numinstances-1)) (or 'all')"
	exit
fi

# Generate SAT solvers and verifiers if necessary
if [ ! -f maplesat_static ] || [ ! -f cadical ] || [ ! -f march_cu ] || [ ! -f gratgen ]
then
	./compile.sh
fi

# Create directories to hold instances and output
mkdir -p base-cnf/$case
mkdir -p a2clauses/$case
mkdir -p cnf/$case
mkdir -p simp-cnf/$case
mkdir -p blocked-cnf/$case
mkdir -p log/$case
mkdir -p proof/$case
mkdir -p cubes/$case
mkdir -p recorded/$case

# Solve all instances in specified range
for i in $range
do
	echo "Generating and solving case $case instance $i..."

	# Get the block selection for this case from a data file (if avilable) or compute it
	if [ -s a2s/$case.block_selection ]
	then
		block_selection=`sed "$((i+1))q;d" a2s/$case.block_selection`
	else
		block_selection=`python2 block_selection.py $case $i`
	fi
	blocks=`echo $block_selection | cut -d' ' -f1`
	maxcol=`echo $block_selection | cut -d' ' -f2`
	inside_blocks=`echo $block_selection | cut -d' ' -f3`

	filename=$case/$case.$blocks-$maxcol.$i

	# Generate SAT instance for given A2 instance #
	make cnf/$filename.cnf

	# Simplify SAT instance
	command="./cadical cnf/$filename.cnf -o simp-cnf/$filename.simp-cnf proof/$filename.simp.proof --no-binary -c 20000 > log/$filename.simp"
	echo $command
	eval $command

	# Check if instance was found to be unsatisfiable
	if [ "$(wc -l simp-cnf/$filename.simp-cnf)" != "2 simp-cnf/$filename.simp-cnf" ]
	then
		# Generate cubes for simplified SAT instance
		numvars=$(./march_cu simp-cnf/$filename.simp-cnf -d 1 -o cubes/$filename.cubes | grep "number of free variables" | cut -d' ' -f7)
		fewervars=`cat data/$case.cutoffs | cut -d' ' -f$((inside_blocks-2))`
		cutoff=$((numvars-fewervars))
		command="./march_cu simp-cnf/$filename.simp-cnf -o cubes/$filename.cubes -n $cutoff | tee log/$filename.$fewervars.cube"
		echo $command
		eval $command

		# Conquer SAT instance using the computed cubes
		command="./maplesat_static -no-pre -assumptions=cubes/$filename.cubes -colmax=$maxcol -recorded=recorded/$filename.recorded simp-cnf/$filename.simp-cnf proof/$filename.solve.proof | tee log/$filename.solve"
		echo $command
		eval $command

		# Combine simplification and conquering proofs together
		cat proof/$filename.simp.proof proof/$filename.solve.proof > proof/$filename.proof

		# Check if any solutions of the SAT instance were recorded
		if [ -s recorded/$filename.recorded ]
		then
			# Add a blocking clause for each solution of the SAT instance recorded
			make blocked-cnf/$filename.blocked-cnf
		else
			# No solutions recorded so verify proof against original SAT instance
			rm recorded/$filename.recorded
			cp cnf/$filename.cnf blocked-cnf/$filename.blocked-cnf
		fi
	else
		# The SAT instance has already been shown unsatisfiable during simplification in this case
		cp proof/$filename.simp.proof proof/$filename.proof
		cp cnf/$filename.cnf blocked-cnf/$filename.blocked-cnf
	fi

	# Verify the DRAT proof that the SAT instance is unsatisfiable
	command="./gratgen blocked-cnf/$filename.blocked-cnf proof/$filename.proof 2> log/$filename.check"
	echo $command
	eval $command
	
	grep "VERIFIED" log/$filename.check
done

