numsplits=1
if [ -z ${1+x} ]
then
	echo "Use ./driver.sh n to enumerate complex Golay pairs of order n>1"
	echo "or ./driver.sh n m to enumerate complex Golay pairs of orders between n and m"
	exit
fi
if [ ! -d bin ]
then
	mkdir bin
fi
if [ -z ${2+x} ]
then
	end=$1
else
	end=$2
fi
for n in `seq $1 $end`
do
	if [ $n -lt 2 ]
	then
		continue
	fi
	# Run preprocessing
	make bin/filtering_evenodd_$n
	bin/filtering_evenodd_$n
	# Run stage 1
	make bin/join_evenodd_$n
	for s in `seq 0 $((numsplits-1))`
	do
		bin/join_evenodd_$n $s
	done
	# Generate data for SAT instances (additional filtering)
	make bin/filter_joins_$n
	for s in `seq 0 $((numsplits-1))`
	do
		bin/filter_joins_$n $s
	done
	# Run stage 2
	for s in `seq 0 $((numsplits-1))`
	do
		python2 constructpairs.py $n $s
	done
	# Run postprocessing
	cat pairs/pairs.$n.*.txt > pairs/pairs.$n.txt
	python2 record_golay_counts.py $n
done
# Print table of counts
python2 print_counts_table.py $1 $end
