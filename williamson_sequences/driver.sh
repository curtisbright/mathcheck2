if [ -z "$1" ]
then
	echo "Use ./driver.sh n to enumerate Williamson sequences of order n divisible by 2, 3, or 5"
	echo "or ./driver.sh n m to enumerate Williamson sequences of orders between n and m (for either even orders or orders 3 mod 6)"
	exit
else
	if [ -z "$2" ]
	then
		u=$1
	else
		u=$2
	fi
	# Runs scripts on even orders if u is even and runs scripts on odd orders if u is odd
	if [ $((u%2)) -eq 0 ]
	then
		d=2
	else
		d=6
	fi
	if [ -z "$3" ]
	then
		c=-1
	else
		c=$3
	fi
	make all
	for n in `seq $1 $d $u`
	do
		./generate_matching_instances_comp $n
		./generate_pairedmatchings $n $c
		./sortpairs.sh $n $c
		./join_pairedmatchings $n $c
		./remove_equivalent_matchedpairs $n $c
		python generate_compstring_instances.py $n $c
		python solve_compstring_instances.py $n $c
		./remove_equivalent_exhaust $n
	done
	python print_timings_table.py $1 $u
fi
