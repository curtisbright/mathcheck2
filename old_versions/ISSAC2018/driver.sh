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
	make bin/filtering_evenodd_$n
	bin/filtering_evenodd_$n
	make bin/join_evenodd_$n
	for s in `seq 0 $((numsplits-1))`
	do
		bin/join_evenodd_$n $s
	done
	for s in `seq 0 $((numsplits-1))`
	do
		python2 constructpairs.py $n $s
	done
	cat pairs/pairs.$n.*.txt > pairs/pairs.$n.txt
	python2 record_golay_counts.py $n
done
