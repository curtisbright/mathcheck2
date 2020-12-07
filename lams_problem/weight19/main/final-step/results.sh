#!/bin/bash

# Script to summarize the results of solving the final collection of SAT instances 

# Ensure that results are read from and output to main directory
if [ ${PWD##*/} == "final-step" ]
then
	# Make main directory the working directory
	cd ..
fi

ALLCASES=(1 2 3 5 6 7 8 9 11 12 13 15 16 17 18 20 21 22 23 24 25 26 27 33 34 36 37 39 41 42 43 46 47 48 49 50 51 53 55 56 58 60 63 65 66)

if [ -z $1 ]
then
	echo "Need case to summarize or 'all' to summarize all times"
	exit
fi

if [ "$1" == "all" ]
then
	range=${ALLCASES[*]}
else
	range=$1
fi

allblocks="1111111"

total=0
total2=0
printf "Case\tSolve\tVerify\t(time in sec)\n"

for case in $range
do
	for maxcol in `seq 58 60`
	do
		if [ -s final-cnf/$case/$case.$allblocks-$maxcol.final-cnf ]
		then
			printf "$case"
			if grep "CPU time" log/$case/$case.$allblocks-$maxcol.solve -q 2>/dev/null
			then
				t=`grep "CPU time" log/$case/$case.$allblocks-$maxcol.solve | xargs | cut -d' ' -f4`
				total=`echo "$total+$t" | bc -l`
				printf "\t%.2f" $t
			else
				printf "\t"
			fi
			if grep "verification time" log/$case/$case.$allblocks-$maxcol.verify -q 2>/dev/null
			then
				t=`grep "verification time" log/$case/$case.$allblocks-$maxcol.verify | cut -d' ' -f4`
				total2=`echo "$total2+$t" | bc -l`
				printf "\t%.2f" $t
			else
				printf "\t"
			fi
			if grep "all lemmas verified, but no conflict" log/$case/$case.$allblocks-$maxcol.verify -q 2>/dev/null
			then
				printf "\tVERIFIED"
			fi
			printf "\n"
			break
		fi
	done
done
if [ "$1" == "all" ]
then
	totalall=`echo "($total+$total2)/3600" | bc -l`
	printf "TOTAL SOLVE:\t%.2f sec\nTOTAL VERIFY:\t%.2f sec\nTOTAL:\t%.2f hours\n" $total $total2 $totalall
fi
