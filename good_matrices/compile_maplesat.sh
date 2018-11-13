if [ ! -d maplesat/maplesat ]
then
	git clone https://bitbucket.org/JLiangWaterloo/maplesat.git
fi
cd maplesat/maplesat
git checkout good-matrices
if [ -z $1 ]
then
	for n in `seq 3 6 69`
	do
		make maplesat_static_$n
	done
	cp simp/maplesat_static_* ../..
else
	make maplesat_static_$1
	cp simp/maplesat_static_$1 ../..
fi
