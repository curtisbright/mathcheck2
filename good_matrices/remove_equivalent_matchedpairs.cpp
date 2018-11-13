#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>
#include <tuple>
#include <array>
#include <set>
#include <sys/types.h>
#include <sys/stat.h>
#include "coprimelist.h"
#include "decomps.h"

#define MAX_N 70

void swap(std::array<int, MAX_N> &A, std::array<int, MAX_N> &B)
{	std::array<int, MAX_N> tmp;
	tmp = A;
	A = B;
	B = tmp;
}

int rowsum(int n, std::array<int, MAX_N> A)
{	int result;
	for(int i=0; i<n; i++)
		result += A[i];
	return result;
}

std::array<int, MAX_N> permuteA(int n, int k, std::array<int, MAX_N> A)
{	std::array<int, MAX_N> result = {};
	for(int i=0; i<n; i++)
	{	result[i] = A[(i*k)%n];
	}
	return result;
}

std::tuple<std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>> minrep(int n, int l, std::array<int, MAX_N> A, std::array<int, MAX_N> B, std::array<int, MAX_N> C, std::array<int, MAX_N> D)
{	
	std::set<std::tuple<std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>>> equivseqns;

	for(int j=0; j<coprimelist_len[n]; j++)
	{	int k = coprimelist[n][j];
		std::array<int, MAX_N> permutedA = permuteA(l, k, A);
		std::array<int, MAX_N> permutedB = permuteA(l, k, B);
		std::array<int, MAX_N> permutedC = permuteA(l, k, C);
		std::array<int, MAX_N> permutedD = permuteA(l, k, D);

		if(permutedC>permutedD)
			swap(permutedC, permutedD);
		if(permutedB>permutedC)
			swap(permutedB, permutedC);
		if(permutedC>permutedD)
			swap(permutedC, permutedD);

		equivseqns.insert(make_tuple(permutedA, permutedB, permutedC, permutedD));
	}

	return *(equivseqns.begin());
}

void fprintseqn(FILE* f, int n, std::tuple<std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>> seqn)
{	
	std::array<int, MAX_N> A;
	std::array<int, MAX_N> B;
	std::array<int, MAX_N> C;
	std::array<int, MAX_N> D;
	std::tie(A, B, C, D) = seqn;

	for(int i=0; i<n; i++)
		fprintf(f, "%d ", A[i]);
	for(int i=0; i<n; i++)
		fprintf(f, "%d ", B[i]);
	for(int i=0; i<n; i++)
		fprintf(f, "%d ", C[i]);
	for(int i=0; i<n; i++)
		fprintf(f, "%d ", D[i]);
	fprintf(f, "\n");
}

int main(int argc, char** argv)
{
	if(argc==1)
		fprintf(stderr, "Need order of matched files to remove equivalences from\n"), exit(0);

	const int n = atoi(argv[1]);

	int casetosolve = -1;
	if(argc>2)
	{	casetosolve = atoi(argv[2]);
	}

	int d;
	if(argc>3)
	{	d = atoi(argv[3]);
	}
	else
	{	if(n%2 == 0)
			d = 2;
		else if(n%3 == 0)
			d = 3;
		else if(n%5 == 0)
			d = 5;
		else if(n%7 == 0)
			d = 7;
		else
			d = 1;
	}
	const int l = n/d;

	int result;
	char filename[100];
	const char seqnsfilename[] = "matchedpairs/%d.%d.%d";
	const char seqnsoutfilename[] = "matchedseqns/%d.%d.%d.inequiv";

	mkdir("timings", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
	mkdir("matchedseqns", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

	printf("ORDER %d: Remove equivalent matched compressions\n", n);
	
	FILE* seqnsfile, * seqnsoutfile;

	for(int c = 0; c < decomps_len[n]; c++)
	{
		if(casetosolve != -1 && casetosolve != c)
			continue;

		sprintf(filename, seqnsoutfilename, n, c, l);
		seqnsoutfile = fopen(filename, "w");

		clock_t start = clock();

		int in, totalcount = 0, inequivcount = 0;
		std::set<std::tuple<std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>>> inequivseqns;
		std::array<int, MAX_N> A = {};
		std::array<int, MAX_N> B = {};
		std::array<int, MAX_N> C = {};
		std::array<int, MAX_N> D = {};

		sprintf(filename, seqnsfilename, n, c, l);
		seqnsfile = fopen(filename, "r");

		while(fscanf(seqnsfile, "%d ", &in)>0)
		{	
			A[0] = in;
			int res;
			for(int i=1; i<l; i++)
			{	res = fscanf(seqnsfile, "%d ", &in);
				A[i] = in;
			}
			for(int i=0; i<l; i++)
			{	res = fscanf(seqnsfile, "%d ", &in);
				B[i] = in;
			}
			for(int i=0; i<l; i++)
			{	res = fscanf(seqnsfile, "%d ", &in);
				C[i] = in;
			}
			for(int i=0; i<l; i++)
			{	res = fscanf(seqnsfile, "%d ", &in);
				D[i] = in;
			}

			std::tuple<std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>> repseqn = minrep(n, l, A, B, C, D);
			if(inequivseqns.count(repseqn)==0)
			{	inequivseqns.insert(repseqn);
				fprintseqn(seqnsoutfile, l, make_tuple(A, B, C, D));
				inequivcount++;
			}

			totalcount++;
		}

		fclose(seqnsfile);

		sprintf(filename, "timings/%d.%d.equivpairstime", n, c);
		FILE* f = fopen(filename, "w");
		fprintf(f, "%.2f\n", (clock() - start)/(float)CLOCKS_PER_SEC);
		fclose(f);

		printf("  Case %d: %d/%d inequivalent matched sequences of length %d output in %.2f seconds\n", c, inequivcount, totalcount, l, (clock() - start)/(float)CLOCKS_PER_SEC);

		fclose(seqnsoutfile);
	}

}
