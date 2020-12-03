#!/bin/bash

# Compile programmatic version MapleSAT tailored to search for A2s (requires the Traces library to compile)
if [ ! -d maplesat ]
then
	git clone https://bitbucket.org/cbright/maplesat.git
fi
cd maplesat
git checkout projplane_w19_a2
cd maplesat
make
cp simp/maplesat_static ../..
cd ../..

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
