#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>
#include <iostream>
#include <tuple>
#include <array>
#include <set>
#include <sys/types.h>
#include <sys/stat.h>
#include "coprimelist.h"
#include "decomps.h"

#define MAX_N 70
#define VERBOSE 0
#define PRINTPAFS 0

#define NDEBUG

int paf(int n, const std::array<int, MAX_N> &A, int s)
{	int res = 0;
	for(int i=0; i<n; i++)
		res += A[i]*A[(i+s)%n];
	return res;
}

void swap(std::array<int, MAX_N> &A, std::array<int, MAX_N> &B)
{	std::array<int, MAX_N> tmp;
	tmp = A;
	A = B;
	B = tmp;
}

void negateA(int n, std::array<int, MAX_N> &A)
{	for(int i=0; i<n; i++)
		A[i] = -A[i];
}

void altnegateA(int n, std::array<int, MAX_N> &A)
{	for(int i=1; i<n; i+=2)
		A[i] = -A[i];
}

std::array<int, MAX_N> permuteA(int n, int k, int s, const std::array<int, MAX_N> &A)
{	std::array<int, MAX_N> result = {};
	for(int i=0; i<n; i++)
	{	result[i] = A[(i*k+s)%n];
	}
	return result;
}

std::tuple<std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>> minrep(int n, int l, const std::array<int, MAX_N> &A, const std::array<int, MAX_N> &B, const std::array<int, MAX_N> &C, const std::array<int, MAX_N> &D)
{	
	std::set<std::tuple<std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>>> equivseqns;

	for(int j=0; j<coprimelist_len[n]; j++)
	{	int k = coprimelist[n][j];
		std::array<int, MAX_N> permutedA = permuteA(l, k, 0, A);
		std::array<int, MAX_N> permutedB = permuteA(l, k, 0, B);
		std::array<int, MAX_N> permutedC = permuteA(l, k, 0, C);
		std::array<int, MAX_N> permutedD = permuteA(l, k, 0, D);

		if(permutedA[0]<0)
			negateA(l, permutedA);

		if(permutedB[0]<0)
			negateA(l, permutedB);

		if(permutedC[0]<0)
			negateA(l, permutedC);

		if(permutedD[0]<0)
			negateA(l, permutedD);

		if(n % 2 == 0)
		{	std::array<int, MAX_N> altpermutedA = permuteA(l, 1, n/2, permutedA);
			std::array<int, MAX_N> altpermutedB = permuteA(l, 1, n/2, permutedB);
			std::array<int, MAX_N> altpermutedC = permuteA(l, 1, n/2, permutedC);
			std::array<int, MAX_N> altpermutedD = permuteA(l, 1, n/2, permutedD);

			if(altpermutedA[0]<0)
				negateA(l, altpermutedA);

			if(altpermutedB[0]<0)
				negateA(l, altpermutedB);

			if(altpermutedC[0]<0)
				negateA(l, altpermutedC);

			if(altpermutedD[0]<0)
				negateA(l, altpermutedD);

			if(permutedA < altpermutedA)
				permutedA = altpermutedA;

			if(permutedB < altpermutedB)
				permutedB = altpermutedB;

			if(permutedC < altpermutedC)
				permutedC = altpermutedC;

			if(permutedD < altpermutedD)
				permutedD = altpermutedD;
		}

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

std::tuple<std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>> minrep_full(int n, int l, std::array<int, MAX_N> &A, std::array<int, MAX_N> &B, std::array<int, MAX_N> &C, std::array<int, MAX_N> &D)
{	
	std::tuple<std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>> rep1 = minrep(n, n, A, B, C, D);
	
	if(n % 2 == 1)
		return rep1;
	else
	{
		altnegateA(n, A);
		altnegateA(n, B);
		altnegateA(n, C);
		altnegateA(n, D);
		
		std::tuple<std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>> rep2 = minrep(n, n, A, B, C, D);

		altnegateA(n, A);
		altnegateA(n, B);
		altnegateA(n, C);
		altnegateA(n, D);
		
		if(rep1 < rep2)
			return rep1;
		else
			return rep2;
	}
}

void fprintseqn(FILE* f, int n, const std::tuple<std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>> &seqn)
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

#if PRINTPAFS==1
int paf(int n, int s, std::array<int, MAX_N> A)
{	int res = 0;
	for(int i=0; i<n; i++)
		res += A[i]*A[(i+s)%n];
	return res;
}

int rowsum(const int n, const std::array<int, MAX_N> &A)
{	int result = 0;
	for(int i=0; i<n; i++)
		result += A[i];
	return result;
}
#endif

void fprettyprintseqn(FILE* f, int n, const std::tuple<std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>> &seqn)
{	
	std::array<int, MAX_N> A;
	std::array<int, MAX_N> B;
	std::array<int, MAX_N> C;
	std::array<int, MAX_N> D;
	std::tie(A, B, C, D) = seqn;

	for(int i=0; i<n; i++)
		fprintf(f, "%c", A[i] == 1 ? '+' : '-');
	fprintf(f, " ");
	for(int i=0; i<n; i++)
		fprintf(f, "%c", B[i] == 1 ? '+' : '-');
	fprintf(f, " ");
	for(int i=0; i<n; i++)
		fprintf(f, "%c", C[i] == 1 ? '+' : '-');
	fprintf(f, " ");
	for(int i=0; i<n; i++)
		fprintf(f, "%c", D[i] == 1 ? '+' : '-');

	#if PRINTPAFS==1
	fprintf(f, " %d %d %d %d |", rowsum(n, A), rowsum(n, B), rowsum(n, C), rowsum(n, D));
	
	fprintf(f, " (");
	for(int i=0; i<n; i++)
		fprintf(f, "%d%s", paf(n, A, i)+paf(n, B, i)+paf(n, C, i)+paf(n, D, i), i<n-1 ? " " : "");
	fprintf(f, ") ");

	fprintf(f, "(");
	for(int i=0; i<n; i++)
		fprintf(f, "%d%s", paf(n, A, i), i<n-1 ? " " : "");
	fprintf(f, ") ");

	fprintf(f, "(");
	for(int i=0; i<n; i++)
		fprintf(f, "%d%s", paf(n, B, i), i<n-1 ? " " : "");
	fprintf(f, ") ");

	fprintf(f, "(");
	for(int i=0; i<n; i++)
		fprintf(f, "%d%s", paf(n, C, i), i<n-1 ? " " : "");
	fprintf(f, ") ");

	fprintf(f, "(");
	for(int i=0; i<n; i++)
		fprintf(f, "%d%s", paf(n, D, i), i<n-1 ? " " : "");
	fprintf(f, ") ");
	#endif

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

	int result;
	char filename[100];
	const char seqnsfilename[] = "exhaust/%d.%d";
	const char seqnsoutfilename[] = "exhaust/%d.inequiv";
	const char seqnsoutfilenamealt[] = "exhaust/%d.%d.inequiv";
	const char seqnsprettyoutfilename[] = "exhaust/good-%d.txt";

	mkdir("timings", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

	FILE* seqnsfile, * seqnsoutfile, * seqnsprettyoutfile;

	int invalidcount = 0;
	
	sprintf(filename, seqnsprettyoutfilename, n);
	seqnsprettyoutfile = fopen(filename, "w");

	if(casetosolve==-1)
		sprintf(filename, seqnsoutfilename, n);
	else
		sprintf(filename, seqnsoutfilenamealt, n, casetosolve);
	seqnsoutfile = fopen(filename, "w");

	int in, totalcount = 0, inequivcount = 0;
	std::set<std::tuple<std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>>> inequivseqns;
	std::array<int, MAX_N> A = {};
	std::array<int, MAX_N> B = {};
	std::array<int, MAX_N> C = {};
	std::array<int, MAX_N> D = {};

	clock_t start = clock();

	for(int c = 0; c < decomps_len[n]; c++)
	{
		if(casetosolve != -1 && casetosolve != c)
			continue;

		sprintf(filename, seqnsfilename, n, c);
		seqnsfile = fopen(filename, "r");
		if(seqnsfile==NULL)
			continue;

		while(fscanf(seqnsfile, "%d ", &in)>0)
		{	
			A[0] = in;
			int res;
			for(int i=1; i<n; i++)
			{	res = fscanf(seqnsfile, "%d ", &in);
				A[i] = in;
			}
			for(int i=0; i<n; i++)
			{	res = fscanf(seqnsfile, "%d ", &in);
				B[i] = in;
			}
			for(int i=0; i<n; i++)
			{	res = fscanf(seqnsfile, "%d ", &in);
				C[i] = in;
			}
			for(int i=0; i<n; i++)
			{	res = fscanf(seqnsfile, "%d ", &in);
				D[i] = in;
			}

			for(int s=1; s<=n/2; s++)
			{	if(paf(n, A, s) + paf(n, B, s) + paf(n, C, s) + paf(n, D, s) != 0)
				{	invalidcount++;
					break;
				}
			}

			std::tuple<std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>, std::array<int, MAX_N>> repseqn = minrep_full(n, n, A, B, C, D);

			#if VERBOSE
			fprettyprintseqn(stdout, n, make_tuple(A, B, C, D));
			printf(" is equivalent to ");
			fprettyprintseqn(stdout, n, repseqn);
			#endif

			if(inequivseqns.count(repseqn)==0)
			{	inequivseqns.insert(repseqn);
				fprintseqn(seqnsoutfile, n, make_tuple(A, B, C, D));
				fprettyprintseqn(seqnsprettyoutfile, n, make_tuple(A, B, C, D));
				fprintf(seqnsprettyoutfile, "\n");
				#if VERBOSE
				printf(" (new)");
				#endif
				inequivcount++;
			}
			#if VERBOSE
			printf("\n");
			#endif

			totalcount++;
		}

		fclose(seqnsfile);

		if(invalidcount > 0)
			printf("  WARNING: Read %d sequences which were not defining rows of good matrices\n", invalidcount);
	}
	fclose(seqnsprettyoutfile);
	fclose(seqnsoutfile);

	sprintf(filename, "timings/%d.equivexhausttime", n);
	FILE* f = fopen(filename, "w");
	fprintf(f, "%.2f\n", (clock() - start)/(float)CLOCKS_PER_SEC);
	fclose(f);

	printf("Order %d: %d/%d inequivalent sequences of length %d output in %.2f seconds\n", n, inequivcount, totalcount, n, (clock() - start)/(float)CLOCKS_PER_SEC);

}
