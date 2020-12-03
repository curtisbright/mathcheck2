#!/bin/bash

# Script to summarize results

totaltime=0
totalcount=0
totalchecktime=0

printf "\t\tTimings (seconds)\n"
printf "Case\t# A2s\tSolve\tVerify\n"

for i in `seq 1 66`
do
	time=0
	count=0
	checktime1=0
	checktime2=0
	if grep "CPU time" log/a2.$i.log -q 2>/dev/null
	then
		time=`cat log/a2.$i.log | grep "CPU time" | xargs | cut -d' ' -f4`
	fi
	if [ -s a2s/$i.complete ]
	then
		count=`wc -l a2s/$i.complete | cut -d' ' -f1`
	fi
	if grep "Overall:" log/a2.$i.check -q 2>/dev/null
	then
		checktime1=`cat log/a2.$i.check | grep "Overall:" | xargs | cut -d' ' -f3`
	fi
	if [ -s log/a2.$i.tracescheck ]
	then
		checktime2=`cat log/a2.$i.tracescheck | cut -d' ' -f16`
	fi
	checktime=`echo "$checktime1/1000+$checktime2" | bc -l`
	totaltime=`echo "$time+$totaltime" | bc -l`
	totalcount=`echo "$count+$totalcount" | bc -l`
	totalchecktime=`echo "$checktime+$totalchecktime" | bc -l`
	printf "$i\t$count\t%.2f\t%.2f\n" $time $checktime
done
printf "TOTAL\t$totalcount\t%.2f\t%.2f\n" $totaltime $totalchecktime
