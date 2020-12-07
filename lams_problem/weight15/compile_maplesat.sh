if [ ! -d maplesat/maplesat ]
then
	git clone https://bitbucket.org/JLiangWaterloo/maplesat.git
fi
cd maplesat/maplesat
if [ ! -f ../../maplesat_static ]
then
	git checkout drup
	make
	cp simp/maplesat_static ../..
fi
git checkout projplane_w15
make
cp simp/maplesat_static ../../maplesat_exhaustive
