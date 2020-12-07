mkdir -p cnf
mkdir -p out
mkdir -p exhaust

# Script to find all 396 nonisomorphic 1-factorizations of the complete graph on ten vertices

if [ ! -f maplesat_exhaustive ]
then
	./compile_maplesat.sh
fi

python projplane_sat.py 1 1 > cnf/b1.cnf

rm exhaust/b1.exhaust

command="./maplesat_exhaustive -no-pre -rowmin=30 -rowmax=66 -colmin=21 -colmax=30 cnf/b1.cnf out/b1.out -exhaustive=exhaust/b1.exhaust"
echo $command
eval $command

