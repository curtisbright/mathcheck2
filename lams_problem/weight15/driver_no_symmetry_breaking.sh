# Driver script using a single CNF instance without using any computer algebra

mkdir -p cnf

m=51
max_columns=75

if [ ! -f maplesat_static ]
then
	./compile_maplesat.sh
fi

if [ -z $1 ]
then
	n=$m
else
	n=$1
fi

python2 projplane_sat.py $n $max_columns > cnf/$n.cnf

command="./maplesat_static cnf/$n.cnf"
echo $command
eval $command

