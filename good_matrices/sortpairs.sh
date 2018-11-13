if [ ! -e tmp/ ]
then
	mkdir tmp/
fi
if [ -z "$1" ]
then
	echo "Need order of PAF files to sort on"
	exit
fi
export LC_ALL=C
n=$1
if [ -n "$3" ]
then
	d=$3
elif [ $((n % 2)) -eq 0 ]
then
	d=2
elif [ $((n % 3)) -eq 0 ]
then
	d=3
elif [ $((n % 5)) -eq 0 ]
then
	d=5
elif [ $((n % 7)) -eq 0 ]
then
	d=7
else
	d=1
fi
l=$((n/d))
echo "ORDER $n: Sort compression pairs"
for c in `seq 0 4`
do
	if [ -n "$2" ] && [ $2 -ne $c ] && [ $2 -ne -1 ]
	then
		continue
	fi
	if [ -e matchings/$n.$c.$l.AB.pafs.txt ]
	then
		START=$(date +%s.%N)
		sort -T tmp/ matchings/$n.$c.$l.AB.pafs.txt > matchings/$n.$c.$l.AB.pafs.sorted.txt
		END=$(date +%s.%N)
		DIFF=$(echo "$END - $START" | bc)
		printf "  Case $c: AB PAFs sorted in %.2f seconds\n" $DIFF
		echo $DIFF > timings/$n.$c.$l.AB.sorttime
	fi
	if [ -e matchings/$n.$c.$l.CD.pafs.txt ]
	then
		START=$(date +%s.%N)
		sort -T tmp/ matchings/$n.$c.$l.CD.pafs.txt > matchings/$n.$c.$l.CD.pafs.sorted.txt
		END=$(date +%s.%N)
		DIFF=$(echo "$END - $START" | bc)
		printf "  Case $c: CD PAFs sorted in %.2f seconds\n" $DIFF
		echo $DIFF > timings/$n.$c.$l.CD.sorttime
	fi
done
