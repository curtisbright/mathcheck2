if [ -z "$1" ]
then
	echo "Use ./driver.sh n to enumerate best matrices of orders n"
	exit
else
	n=$1
	if [ $((n%2)) -eq 0 ]
	then
		echo "Warning: Order must be odd"
	elif [ $((n%3)) -ne 0 ]
	then
		echo "Warning: Order is not divisible by 3, not using compression"
	fi
	make all
	./generate_matching_instances_comp $n
	./generate_pairedmatchings $n
	./sortpairs.sh $n
	./join_pairedmatchings $n
	./remove_equivalent_matchedpairs $n
	python2 generate_compstring_instances.py $n
	python2 solve_compstring_instances.py $n
	./remove_equivalent_exhaust $n
	python2 print_timings_table.py $n
fi
