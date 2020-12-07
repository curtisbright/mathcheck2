# Driver script using a single CNF instance and assumptions for each solution of first 27 lines

mkdir -p cnf
mkdir -p exhaust

m=51
max_columns=75

if [ ! -f maplesat_exhaustive ]
then
	./compile_maplesat.sh
fi

python projplane_sat.py 27 $max_columns > cnf/27.cnf

if [ -f exhaust/27.exhaust ]
then
	rm exhaust/27.exhaust
fi

command="./maplesat_exhaustive -no-pre cnf/27.cnf -rowmin=21 -rowmax=27 -colmin=15 -colmax=75 -eager -exhaustive=exhaust/27.exhaust"
echo $command
eval $command

if [ -z $1 ]
then
	n=$m
else
	n=$1
fi

python projplane_sat.py $n $max_columns > cnf/$n.cnf

command="./maplesat_exhaustive cnf/$n.cnf -no-pre -assumptions=exhaust/27.exhaust -addunits -no-isoblock -verb=0"
echo $command
eval $command

