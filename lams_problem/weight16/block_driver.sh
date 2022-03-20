#!/bin/bash
mkdir -p cubes
mkdir -p log
mkdir -p out

genproof=false

set -o pipefail

if [ -z $1 ]
then
	echo "Need case to run (1a, 1b, 1c) and optionally instance # of first block to solve"
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

# Automatic parameter selection based on case
if [ "$case" == "1a" ]
then
	b=875
	cols=23
	num=275
elif [ "$case" == "1b" ]
then
	b=800
	cols=24
	num=275
elif [ "$case" == "1c" ]
then
	b=800
	cols=24
	num=469
fi

if [ ! -z $3 ]
then
	b=$3	# Custom cubing bound
fi

# Generate SAT instance
if [ ! -s cnf/$case.blocking.combine.cnf ]
then
	./gen_blocking_instance.sh $case
fi

# Simplify SAT instance
if [ ! -s cnf/$case.simp.cnf ]
then
	command="./lingeling cnf/$case.cnf -q -s -O5 -o cnf/$case.simp.cnf -t out/$case.simp.out"
	echo $command
	eval $command
fi

if [ -z $2 ]
then
	range=`seq 0 $((num-1))`
else
	range=`seq $2 $2`
fi

# Solve SAT instances
for i in $range
do
	# Generate assumptions to specify the variables in the first block
	# Hack: A few default representatives produce satisfiable instances so use alternative representatives in those cases
	if [ $case == "1a" ] && [ $i -eq 171 ]
	then
		python2 expand.py exhaust/$case.$cols.exhaust-blocking.sorted $i 3 > assums/$case.$i.assums
	elif [ $case == "1c" ] && ([ $i -eq 63 ] || [ $i -eq 103 ])
	then
		python2 expand.py exhaust/$case.$cols.exhaust-blocking.sorted $i 1 > assums/$case.$i.assums
	else
		python2 expand.py exhaust/$case.$cols.exhaust-blocking.sorted $i 0 > assums/$case.$i.assums
	fi
	
	# In case 1b use symmetry breaking clauses in the instance given to cubing solver
	if [ $case == "1b" ]
	then
		# Generate SAT instance for case 1b and instance # i
		cat cnf/$case.blocking.combine.cnf assums/$case.$i.assums > cnf/$case.blocking.combine.$i.cnf
		# Setting variable 8881+i to false tells the SAT solver that we are solving case i (and therefore all blocks must have labels >= i)
		echo "-$((8881+i)) 0" >> cnf/$case.blocking.combine.$i.cnf
		numclauses=$(wc -l cnf/$case.blocking.combine.$i.cnf | cut -d ' ' -f1)
		sed -i -E "s/p cnf ([0-9]*) ([0-9]*)/p cnf \1 $((numclauses-1))/" cnf/$case.blocking.combine.$i.cnf

		# Simplify instance with symmetry breaking clauses
		command="./lingeling cnf/$case.blocking.combine.$i.cnf -q -s -O5 -o cnf/$case.blocking.combine.$i.simp.cnf -t /dev/null | tee log/$case.$i.$b.simp"
		echo $command
		eval $command

		# Generate cubes
		command="./march_cu cnf/$case.blocking.combine.$i.simp.cnf -n $b -o cubes/$case.$i.$b.cubes | tee log/$case.$i.$b.cube"
		echo $command
		eval $command
		rm cnf/$case.blocking.combine.$i.cnf cnf/$case.blocking.combine.$i.simp.cnf
	# In cases 1a and 1c do not use the symmetry breaking clauses in the cubing step
	else
		cat cnf/$case.simp.cnf assums/$case.$i.assums > cnf/$case.simp.$i.cnf
		numclauses=$(wc -l cnf/$case.simp.$i.cnf | cut -d ' ' -f1)
		sed -i -E "s/p cnf ([0-9]*) ([0-9]*)/p cnf \1 $((numclauses-1))/" cnf/$case.simp.$i.cnf

		# Generate cubes
		if [ ! -s cubes/$case.$i.$b.cubes ]
		then
			command="./march_cu cnf/$case.simp.$i.cnf -n $b -o cubes/$case.$i.$b.cubes | tee log/$case.$i.$b.cube"
			echo $command
			eval $command
		fi
	fi

	# Solve instance using cube-and-conquer
	if [ ! -s out/$case.$i.$b.out ]
	then
		# Generate assumptions to specify the variables in the first block
		# Hack: A few default representatives produce satisfiable instances so use alternative representatives in those cases
		if [ $case == "1a" ] && [ $i -eq 171 ]
		then
			hardassums=$(python2 expand.py -commas exhaust/$case.$cols.exhaust-blocking.sorted $i 3)
		elif [ $case == "1c" ] && ([ $i -eq 63 ] || [ $i -eq 103 ])
		then
			hardassums=$(python2 expand.py -commas exhaust/$case.$cols.exhaust-blocking.sorted $i 1)
		else
			hardassums=$(python2 expand.py -commas exhaust/$case.$cols.exhaust-blocking.sorted $i 0)
		fi
		# Setting variable 8881+i to false tells the SAT solver that we are solving case i (and therefore all blocks must have labels >= i)
		hardassums="$hardassums,-$((8881+i))"
		if $genproof
		then
			proofout="out/$case.$i.$b.out "
		fi
		solvecommand="./maplesat_static_$case -assumptions=cubes/$case.$i.$b.cubes cnf/$case.blocking.combine.cnf -hardassums=$hardassums -verb=0 -reduce-frac=10 -print-bound=10 $proofout| tee log/$case.$i.$b.pre.solve"
		echo $solvecommand
		eval $solvecommand
		result=$?
	else
		result=20
	fi

	# Verify proof if generated
	if [ $result -eq 20 ] && $genproof
	then
		# Generate single contained SAT instance for instance # i
		cat cnf/$case.blocking.combine.cnf assums/$case.$i.assums > cnf/$case.$i.block.cnf
		echo "-$((8881+i)) 0" >> cnf/$case.$i.block.cnf
		numclauses=$(wc -l cnf/$case.$i.block.cnf | cut -d ' ' -f1)
		sed -i -E "s/p cnf ([0-9]*) ([0-9]*)/p cnf \1 $((numclauses-1))/" cnf/$case.$i.block.cnf

		# Verify proof if generated
		if [ ! -s out/$case.$i.$b.trim.out ]
		then
			checkcommand="./drat-trim cnf/$case.$i.block.cnf out/$case.$i.$b.out -w -C -b -l out/$case.$i.$b.trim.out | tee log/$case.$i.$b.check"
			echo $checkcommand
			eval $checkcommand                                                       
			result=$?
		else
			result=0
		fi

		# Compress proof in 7z archive
		if [ $result -eq 0 ]
		then
			compresscommand="7z a out/$case.$i.$b.trim.out.7z $PWD/out/$case.$i.$b.trim.out | tee log/$case.$i.$b.compress"
			echo $compresscommand
			eval $compresscommand
			result=$?

			# Remove uncompressed proof if archiving succeeded
			if [ $result -eq 0 ]
			then
				rm out/$case.$i.$b.out out/$case.$i.$b.trim.out
			fi
		fi
	fi
done
