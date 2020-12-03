#!/bin/bash

# Script to summarize the results of solving each SAT instance for a given case

if [ -z $1 ]
then
	echo "Need case to summarize results for"
	exit
fi

case=$1
numinstances=`cat a2s/$case.complete | wc -l`

range=`seq 0 $((numinstances-1))`

total=0
total2=0
printf "Case\tSimp\tCube\tSolve\tVerify\t(time in sec)\n"

for instno in $range
do
	block_selection=`python block_selection.py $case $instno`
	blocks=`echo $block_selection | cut -d' ' -f1`
	maxcol=`echo $block_selection | cut -d' ' -f2`
	inside_blocks=`echo $block_selection | cut -d' ' -f3`
	fewervars=`cat data/$case.cutoffs | cut -d' ' -f$((inside_blocks-2))`

	printf "$case-$instno"
	if grep "total process time since" log/$case/$case.$blocks-$maxcol.$instno.simp -q 2>/dev/null
	then
		t=`grep "total process time since" log/$case/$case.$blocks-$maxcol.$instno.simp | xargs | cut -d' ' -f7`
		total=`echo "$total+$t" | bc -l`
		printf "\t%.2f" $t
	else
		printf "\t"
	fi
	if grep "c time" log/$case/$case.$blocks-$maxcol.$instno.$fewervars.cube -q 2>/dev/null
	then
		t=`grep "c time" log/$case/$case.$blocks-$maxcol.$instno.$fewervars.cube | cut -d' ' -f4`
		total=`echo "$total+$t" | bc -l`
		printf "\t%.2f" $t
	else
		printf "\t"
	fi
	if grep "CPU time" log/$case/$case.$blocks-$maxcol.$instno.solve -q 2>/dev/null
	then
		t=`grep "CPU time" log/$case/$case.$blocks-$maxcol.$instno.solve | xargs | cut -d' ' -f4`
		total=`echo "$total+$t" | bc -l`
		printf "\t%.2f" $t
	else
		printf "\t"
	fi
	if grep "c Overall" log/$case/$case.$blocks-$maxcol.$instno.check -q 2>/dev/null
	then
		t=`grep "c Overall" log/$case/$case.$blocks-$maxcol.$instno.check | xargs | cut -d' ' -f3`
		tsec=`echo "($t)/1000" | bc -l`
		total2=`echo "$total2+$tsec" | bc -l`
		printf "\t%.2f" $tsec
	else
		printf "\t"
	fi
	if grep "all lemmas verified, but no conflict" log/$case/$case.$blocks-$maxcol.$instno.verify -q 2>/dev/null
	then
		printf "\tVERIFIED"
	fi
	printf "\n"
done
totalall=`echo "($total+$total2)/3600" | bc -l`
printf "TOTAL SOLVE:\t%.2f sec\nTOTAL VERIFY:\t%.2f sec\nTOTAL:\t%.2f hours\n" $total $total2 $totalall
