#!/bin/bash

# Script to summarize results

totalgentime=0
totalvertime=0
totalsoltime=0
totalchetime=0
totalreccount=0
totalrejcount=0

printf "                                 Timings (seconds)         \n"
printf "           A2 counts      Nonisomorphic      Pure SAT Inst.\n"
printf " Case  Inequiv.   Total Generate   Verify    Solve   Verify\n"

for i in `seq 1 66`
do
	gentime=0
	vertime=0
	soltime=0
	chetime=0
	reccount=0
	rejcount=0
	if grep "CPU time" log/$i.noniso-generate.log -q 2>/dev/null
	then
		gentime=`cat log/$i.noniso-generate.log | grep "CPU time" | xargs | cut -d' ' -f4`
	fi
	if grep "CPU time" log/$i.noniso-verify.log -q 2>/dev/null
	then
		vertime=`cat log/$i.noniso-verify.log | grep "CPU time" | xargs | cut -d' ' -f4`
	fi
	if grep "CPU time" log/$i.allblock.log -q 2>/dev/null
	then
		soltime=`cat log/$i.allblock.log | grep "CPU time" | xargs | cut -d' ' -f4`
	fi
	if grep "Overall:" log/$i.allblock.check -q 2>/dev/null
	then
		chetime=`cat log/$i.allblock.check | grep "Overall:" | xargs | cut -d' ' -f3`
		chetime=`echo "$chetime/1000" | bc -l`
	fi
	if [ -s out/$i.recorded ]
	then
		reccount=`wc -l out/$i.recorded | cut -d' ' -f1`
	fi
	if [ -s out/$i.rejected ]
	then
		rejcount=`wc -l out/$i.rejected | cut -d' ' -f1`
	fi
	totalgentime=`echo "$gentime+$totalgentime" | bc -l`
	totalvertime=`echo "$vertime+$totalvertime" | bc -l`
	totalsoltime=`echo "$soltime+$totalsoltime" | bc -l`
	totalchetime=`echo "$chetime+$totalchetime" | bc -l`
	totalreccount=`echo "$reccount+$totalreccount" | bc -l`
	totalrejcount=`echo "$rejcount+$totalrejcount" | bc -l`
	printf "%5d %8d %8d %8.1f %8.1f %8.1f %8.1f\n" $i $reccount $((reccount+rejcount)) $gentime $vertime $soltime $chetime
done
printf "TOTAL %8d %8d %8.1f %8.1f %8.1f %8.1f\n" $totalreccount $((totalreccount+totalrejcount)) $totalgentime $totalvertime $totalsoltime $totalchetime
