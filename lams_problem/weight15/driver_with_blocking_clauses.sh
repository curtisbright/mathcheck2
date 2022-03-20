# Driver script using a single CNF instance blocking each nonisomorphic solution of first 27 lines

mkdir -p cnf
mkdir -p exhaust

m=51
max_columns=75

if [ ! -f maplesat_exhaustive ] || [ ! -f maplesat_static ]
then
	./compile_maplesat.sh
fi

python2 projplane_sat.py 27 $max_columns > cnf/27.cnf

if [ -f exhaust/27.exhaust ]
then
	rm exhaust/27.exhaust
fi

if [ -f exhaust/27.exhaust2 ]
then
	rm exhaust/27.exhaust2
fi

command="./maplesat_exhaustive -no-pre cnf/27.cnf -rowmin=21 -rowmax=27 -colmin=15 -colmax=75 -exhaustive=exhaust/27.exhaust -exhaustive2=exhaust/27.exhaust2"
echo $command
eval $command

if [ -z $1 ]
then
	n=$m
else
	n=$1
fi

python2 projplane_sat.py $n $max_columns > cnf/$n.cnf

cat cnf/$n.cnf exhaust/27.exhaust2 > cnf/$n.blocking.cnf
numclauses=$(wc -l < cnf/$n.blocking.cnf)
numclauses=$((numclauses-1))
sed -i -E "s/p cnf ([0-9]*) ([0-9]*)/p cnf \1 $numclauses/" cnf/$n.blocking.cnf

command="./maplesat_static -no-pre cnf/$n.blocking.cnf"
echo $command
eval $command

