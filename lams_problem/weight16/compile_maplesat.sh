#!/bin/sh
if [ ! -d maplesat/maplesat ]
then
	git clone https://bitbucket.org/JLiangWaterloo/maplesat.git
fi
cd maplesat/maplesat
git checkout projplane_w16
make
cp -f simp/maplesat_static_1a ../..
cp -f simp/maplesat_static_1b ../..
cp -f simp/maplesat_static_1c ../..
cp -f simp/maplesat_static_1a ../../maplesat_static
cd ../..
