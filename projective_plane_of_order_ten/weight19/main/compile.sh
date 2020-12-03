#!/bin/bash

# Compile MapleSAT to perform exhaustive search for solutions of main instances
if [ ! -d maplesat ]
then
	git clone https://bitbucket.org:cbright/maplesat.git
fi
cd maplesat
git checkout projplane_w19_main
cd maplesat
make
cp simp/maplesat_static ../..
cd ../..

# Compile march_cu SAT solver (for cubing)
if [ ! -d CnC ]
then
	git clone https://github.com:curtisbright/CnC.git
fi
cd CnC
git checkout w19
cd march_cu
make
cp march_cu ../..
cd ../..

# Compile CaDiCaL SAT solver (for simplification)
if [ ! -d cadical-dir ]
then
	git clone https://github.com:curtisbright/cadical.git cadical-dir
fi
cd cadical-dir
if [ ! -f makefile ]
then
	./configure
fi
make
cp build/cadical ..
cd ..

# Compile DRAT-trim proof verifier
if [ ! -d drat-trim-dir ]
then
	git clone https://github.com:curtisbright/drat-trim.git drat-trim-dir
fi
cd drat-trim-dir
make
cp drat-trim ..
cd ..

# Compile GRATgen proof verifier
if [ ! -d gratgen-dir ]
then
	git clone https://github.com:curtisbright/gratgen.git gratgen-dir
fi
cd gratgen-dir
git checkout noboost
make -f makefile-simple
cp gratgen ..
cd ..
