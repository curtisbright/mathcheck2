CCOMP = cc
CPPCOMP = c++
PHONY:
	@echo "Use ./driver.sh n to enumerate complex Golay pairs of order n>1"
maplesat_static: compile_maplesat.sh
	./compile_maplesat.sh
bin/filtering_evenodd_%: filtering_evenodd.c
	$(CCOMP) filtering_evenodd.c -o $@ -std=gnu99 -lm -lfftw3 -Ofast -DN=$*
bin/join_evenodd_%: join_evenodd.cpp squaredecompfilter.h
	$(CPPCOMP) join_evenodd.cpp -o $@ -std=gnu++0x -lm -lfftw3 -Ofast -DN=$*
clean:
	rm -rf bin
