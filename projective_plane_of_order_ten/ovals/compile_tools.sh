mkdir -p tools
cd tools
if [ ! -f ../march_cu ] || [ ! -f ../lingeling ]
then
	if [ ! -d CnC ]
	then
		git clone https://github.com/curtisbright/CnC.git
	fi
	cd CnC
	git checkout w12
	if [ ! -f lingeling-bbc-9230380-160707-druplig-009.tar.gz ]
	then
		wget http://fmv.jku.at/lingeling/lingeling-bbc-9230380-160707-druplig-009.tar.gz
	fi
	if [ ! -d lingeling-bbc-9230380-160707-druplig-009 ]
	then
		tar --extract --file lingeling-bbc-9230380-160707-druplig-009.tar.gz
		cd lingeling-bbc-9230380-160707-druplig-009
		./extract-and-compile.sh
		mv druplig ..
		cd ..
	fi
	if [ $(cat lingeling/lglmain.c | wc -l) -eq 587 ]
	then
		sed -i '532i  if(!simponly)' lingeling/lglmain.c
	fi
	./build.sh
	cp march_cu/march_cu ../..
	cp lingeling/lingeling ../..
	cd ..
fi
if [ ! -f ../drat-trim ]
then
	if [ ! -d drat-trim ]
	then
		git clone https://github.com/curtisbright/drat-trim.git
	fi
	cd drat-trim
	git checkout trust
	make
	cp drat-trim ../..
	cd ..
fi
if [ ! -d maplesat/maplesat ]
then
	git clone https://bitbucket.org/JLiangWaterloo/maplesat.git
fi
if [ ! -f ../maplesat_static ]
then
	cd maplesat/maplesat
	git checkout projplane_w12
	make
	cp -f simp/maplesat_static ../../..
fi
