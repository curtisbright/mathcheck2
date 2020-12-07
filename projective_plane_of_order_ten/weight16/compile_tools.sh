mkdir -p tools
cd tools

if [ ! -s ../march_cu ] || [ ! -s ../lingeling ]
then
	if [ ! -d CnC ]
	then
		git clone https://github.com/curtisbright/CnC.git
	fi
	cd CnC
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
	make
	cp drat-trim ../..
fi
