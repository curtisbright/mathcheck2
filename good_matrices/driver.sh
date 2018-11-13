if [ -z "$1" ]
then
	echo "Use ./driver.sh n to enumerate good matrices of odd orders n divisible by 3"
	echo "or ./driver.sh n m to enumerate good matrices of odd orders between n and m divisible by 3"
	exit
else
	if [ -z "$2" ]
	then
		u=$1
	else
		u=$2
	fi
	if [ $((u%2)) -eq 0 ]
	then
		echo "Order must be odd"
		exit
	elif [ $((u%3)) -ne 0 ]
	then
		echo "Order must be divisible by 3"
		exit
	fi
	make all
	for n in `seq $1 6 $u`
	do
		./generate_matching_instances_comp $n
		./generate_pairedmatchings $n
		./sortpairs.sh $n
		./join_pairedmatchings $n
		./remove_equivalent_matchedpairs $n
		python generate_compstring_instances.py $n
		python solve_compstring_instances.py $n
		./remove_equivalent_exhaust $n
	done
	python print_timings_table.py $1 $u
fi
