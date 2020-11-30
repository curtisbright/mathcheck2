if [ ! -d maplesat/maplesat ]
then
	git clone https://bitbucket.org/JLiangWaterloo/maplesat.git
fi
cd maplesat/maplesat
git checkout w12_exhaustive
make
cp -f simp/maplesat_static ../../maplesat_exhaustive
cd ../..
