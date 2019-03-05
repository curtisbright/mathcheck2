if [ ! -d maplesat/maplesat ]
then
	git clone https://bitbucket.org/JLiangWaterloo/maplesat.git
fi
cd maplesat/maplesat
git checkout best-matrices
if [ -z $1 ]
then
	echo "Need the order of best matrices to search for"
else
	make maplesat_static_$1
	cp simp/maplesat_static_$1 ../..
fi
