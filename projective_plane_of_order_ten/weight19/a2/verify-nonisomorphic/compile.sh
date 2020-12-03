#!/bin/bash

# Compile programmatic version MapleSAT tailored to enumerate all nonisomorphic A2s (without using Traces)
if [ ! -d maplesat ]
then
	git clone https://bitbucket.org:cbright/maplesat.git
fi
cd maplesat
git checkout projplane_w19_notraces
cd maplesat
make
cp simp/maplesat_static ../..
cd ../..

# Compile GRATgen proof verifier
if [ ! -d ../gratgen-dir ]
then
	git clone https://github.com:curtisbright/gratgen.git ../gratgen-dir
fi
cd ../gratgen-dir
git checkout noboost
make -f makefile-simple
cp gratgen ../verify-nonisomorphic
cd ../verify-nonisomorphic
