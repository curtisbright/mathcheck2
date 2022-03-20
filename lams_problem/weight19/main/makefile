SHELL := /bin/bash
.SECONDARY:
.SECONDEXPANSION:
base-cnf/%.base-cnf:
	@case=`echo $* | cut -d'/' -f1`; \
	blocks=`echo $* | cut -d'.' -f2 | cut -d'-' -f1`; \
	maxcol=`echo $* | cut -d'.' -f2 | cut -d'-' -f2`; \
	command="python2 satgen_main.py $$case $$blocks $$maxcol > $@"; \
	echo $$command; \
	eval $$command;
a2clauses/%.a2clauses:
	@case=`echo $* | cut -d'/' -f1`; \
	blocks=`echo $* | cut -d'.' -f2 | cut -d'-' -f1`; \
	i=`echo $* | cut -d'.' -f3`; \
	command="python2 a2_clauses.py $$case $$blocks $$i > $@"; \
	eval $$command;
cnf/%.cnf: base-cnf/$$(basename %).base-cnf a2clauses/%.a2clauses
	@VARS=`tail a2clauses/$*.a2clauses -n 1 | cut -d' ' -f6`; \
	LEN1=`head base-cnf/$(basename $*).base-cnf -n 1 | cut -d' ' -f4`; \
	LEN2=`wc -l a2clauses/$*.a2clauses | cut -d' ' -f1`; \
	echo "p cnf $$VARS $$((LEN1+LEN2-1))" > $@; \
	tail -n +2 base-cnf/$(basename $*).base-cnf >> $@; \
	cat a2clauses/$*.a2clauses >> $@;
blocked-cnf/%.blocked-cnf: recorded/%.recorded
	@VARS=`tail cnf/$*.cnf -n 1 | cut -d' ' -f6`; \
	LEN1=`head cnf/$*.cnf -n 1 | cut -d' ' -f4`; \
	LEN2=`wc -l recorded/$*.recorded | cut -d' ' -f1`; \
	echo "p cnf $$VARS $$((LEN1+LEN2))" > $@; \
	tail -n +2 cnf/$*.cnf >> $@; \
	sed 's/ / -/g; s/-0/0/g; s/a //g' recorded/$*.recorded >> $@;
final-cnf/%.final-cnf:
	@case=`echo $* | cut -d'/' -f1`; \
	blocks=`echo $* | cut -d'.' -f2 | cut -d'-' -f1`; \
	maxcol=`echo $* | cut -d'.' -f2 | cut -d'-' -f2`; \
	command="python2 satgen_main.py $$case $$blocks $$maxcol -no-lex > $@"; \
	echo $$command; \
	eval $$command;
recorded/%.recorded-full: recorded/%.recorded cnf/%.cnf
	@maxcol=`echo $* | cut -d'.' -f2 | cut -d'-' -f2`; \
	./maplesat_static -no-pre -assumptions=$< cnf/$*.cnf -recorded=$@ -colmin=20 -colmax=$$maxcol > /dev/null || true;
final-cnf/%.assums: $$(wildcard recorded/$$(dir %)*.recorded)
	@case=`echo $* | cut -d'/' -f1`; \
	rm $@ 2>/dev/null; \
	for f in recorded/$$case/*.recorded; do \
		blocks=`echo $$f | cut -d'.' -f2 | cut -d'-' -f1`; \
		maxcol=`echo $$f | cut -d'.' -f2 | cut -d'-' -f2`; \
		instno=`echo $$f | cut -d'.' -f3`; \
		oppblocks=`sed 's/1/2/g; s/0/1/g; s/2/0/g' <<< $$blocks`; \
		make $$f-full --no-print-directory; \
		make a2clauses/$$case/$$case.$$oppblocks-$$maxcol.$$instno.a2clauses --no-print-directory; \
		a2assums=`sed -n '/^[[:digit:]][^ ]* 0$$/p' a2clauses/$$case/$$case.$$oppblocks-$$maxcol.$$instno.a2clauses | sed 's/ 0//' | tr '\n' ' '`; \
		sed "s/^a /a $$a2assums/" $$f-full >> $@; \
	done;
