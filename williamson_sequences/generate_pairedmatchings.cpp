#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>
#include <fftw3.h>
#include <sys/types.h>
#include <sys/stat.h>
#include "decomps.h"

#define VERBOSE 0
#ifndef NUMSPLITS
#define NUMSPLITS 1
#endif
#if !defined(AB) && !defined(CD)
#define ABCD
#endif

const int MAX_N = 70;
const int HALF_MAX_N = 1+MAX_N/2;
#include <array>
#include <vector>
//#include <tuple>
//#include <algorithm>

#if VERBOSE==1
void printseqnpsds(int n, int* A, int* B, int* C, int* D)
{	
	double* fft_signal = (double*)malloc(sizeof(double)*n);
	fftw_complex* fft_result = (fftw_complex*)malloc(sizeof(fftw_complex)*n);
	fftw_plan plan = fftw_plan_dft_r2c_1d(n, fft_signal, fft_result, FFTW_ESTIMATE);

	double psds[n/2+1];
	for(int i=0; i<=n/2; i++)
		psds[i] = 0;

	for(int i=0; i<n; i++)
		printf("%d ", A[i]);
	for(int i=0; i<n; i++)
		printf("%d ", B[i]);
	for(int i=0; i<n; i++)
		printf("%d ", C[i]);
	for(int i=0; i<n; i++)
		printf("%d ", D[i]);

	for(int i=0; i<n; i++)
		fft_signal[i] = A[i];
	fftw_execute(plan);
	for(int i=0; i<=n/2; i++)
		psds[i] += fft_result[i][0]*fft_result[i][0];

	for(int i=0; i<n; i++)
		fft_signal[i] = B[i];
	fftw_execute(plan);
	for(int i=0; i<=n/2; i++)
		psds[i] += fft_result[i][0]*fft_result[i][0];

	for(int i=0; i<n; i++)
		fft_signal[i] = C[i];
	fftw_execute(plan);
	for(int i=0; i<=n/2; i++)
		psds[i] += fft_result[i][0]*fft_result[i][0];

	for(int i=0; i<n; i++)
		fft_signal[i] = D[i];
	fftw_execute(plan);
	for(int i=0; i<=n/2; i++)
		psds[i] += fft_result[i][0]*fft_result[i][0];

	printf(": ");
	for(int i=0; i<=n/2; i++)
		printf("%.2f ", psds[i]);

	printf("\n");

	fftw_destroy_plan(plan);
	free(fft_signal);
	free(fft_result);
}

void printApsds(int n, int* A)
{	
	double* fft_signal = (double*)malloc(sizeof(double)*n);
	fftw_complex* fft_result = (fftw_complex*)malloc(sizeof(fftw_complex)*n);
	fftw_plan plan = fftw_plan_dft_r2c_1d(n, fft_signal, fft_result, FFTW_ESTIMATE);

	double psds[n/2+1];
	for(int i=0; i<=n/2; i++)
		psds[i] = 0;

	for(int i=0; i<n; i++)
		printf("%d ", A[i]);

	for(int i=0; i<n; i++)
		fft_signal[i] = A[i];
	fftw_execute(plan);
	for(int i=0; i<=n/2; i++)
		psds[i] += fft_result[i][0]*fft_result[i][0];

	printf(": ");
	for(int i=0; i<=n/2; i++)
		printf("%.2f ", psds[i]);

	printf("\n");

	fftw_destroy_plan(plan);
	free(fft_signal);
	free(fft_result);
}
#endif

void printA(int n, int* A)
{	for(int i=0; i<n; i++)
		printf("%d ", A[i]);
	printf("\n");
}

void printA(int n, double* A)
{	for(int i=0; i<n; i++)
		printf("%.15f ", A[i]);
	printf("\n");
}

void printseqn(int n, int* A, int* B, int* C, int* D)
{	for(int i=0; i<n; i++)
		printf("%d ", A[i]);
	for(int i=0; i<n; i++)
		printf("%d ", B[i]);
	for(int i=0; i<n; i++)
		printf("%d ", C[i]);
	for(int i=0; i<n; i++)
		printf("%d ", D[i]);
	printf("\n");
}

void fprintpair(FILE* f, int n, int* A, int iA, int iB)
{	for(int i=0; i<n; i++)
		fprintf(f, "%d ", A[i]);
	fprintf(f, ": %d %d\n", iA, iB);
}

void fprintseqn(FILE* f, int n, int* A, int* B, int* C, int* D)
{	for(int i=0; i<n; i++)
		fprintf(f, "%d ", A[i]);
	for(int i=0; i<n; i++)
		fprintf(f, "%d ", B[i]);
	for(int i=0; i<n; i++)
		fprintf(f, "%d ", C[i]);
	for(int i=0; i<n; i++)
		fprintf(f, "%d ", D[i]);
	fprintf(f, "\n");
}

void fprintseqn(FILE* f, int n, int* A)
{	
	for(int i=0; i<n; i++)
		fprintf(f, "%d ", A[i]);
	fprintf(f, "\n");
}

int main(int argc, char** argv)
{
	char filename[100];
	int n1, n2;

	if(argc==1)
		fprintf(stderr, "Need order of paired matchings files to compute\n"), exit(0);

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
		else
			fprintf(stderr, "Invalid divisor\n"), exit(0);
	}
	const int l = n/d;

	#if NUMSPLITS == 1
	const int splitcase = 0;
	#else
	if(argc<=4)
		fprintf(stderr, "Need case # of split file to compute\n"), exit(0);
	const int splitcase = atoi(argv[4]);
	if(splitcase>=NUMSPLITS)
		fprintf(stderr, "Invalid split case #\n"), exit(0);
	#endif

	const char seqnsfilename[] = "matchings/%d.%d.%d.%s.seqns.txt";
	const char pafsfilename[] = "matchings/%d.%d.%d.%s.pafs.txt";
	#if NUMSPLITS > 1
	const char pairedpafsfilename[] = "matchings/%d.%d.%d.%s.%d.pafs.txt";
	#endif

	mkdir("timings", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

	const int pafslen = l/2+1;

	printf("ORDER %d: Generate compression sequence pairs\n", n);

	double* fft_signal = (double*)malloc(sizeof(double)*l);
	fftw_complex* fft_result = (fftw_complex*)malloc(sizeof(fftw_complex)*l);
	fftw_plan plan = fftw_plan_dft_r2c_1d(l, fft_signal, fft_result, FFTW_ESTIMATE);

	for(int c = 0; c < decomps_len[n]; c++)
	{
		if(casetosolve != -1 && casetosolve != c)
			continue;

		FILE* seqnsfile;
		FILE* pafsfile;

		std::vector<std::array<int, MAX_N>> Aseqns;
		std::vector<std::array<int, MAX_N>> Bseqns;
		std::vector<std::array<int, MAX_N>> Cseqns;
		std::vector<std::array<int, MAX_N>> Dseqns;
		std::vector<std::array<double, HALF_MAX_N>> Apsdslist;
		std::vector<std::array<double, HALF_MAX_N>> Bpsdslist;
		std::vector<std::array<double, HALF_MAX_N>> Cpsdslist;
		std::vector<std::array<double, HALF_MAX_N>> Dpsdslist;
		std::vector<std::array<int, HALF_MAX_N>> Apafs;
		std::vector<std::array<int, HALF_MAX_N>> Bpafs;
		std::vector<std::array<int, HALF_MAX_N>> Cpafs;
		std::vector<std::array<int, HALF_MAX_N>> Dpafs;

		std::array<int, MAX_N> X = {};
		std::array<double, HALF_MAX_N> psds = {};
		std::array<int, HALF_MAX_N> P = {};
		std::array<int, HALF_MAX_N> ABpafs;
		std::array<int, HALF_MAX_N> CDpafs;

		int in, i;
		char filename[100];

		clock_t start = clock();
		#if defined(AB) || defined(ABCD)
		int splitcount = 0;

		sprintf(filename, seqnsfilename, n, c, l, "A");
		seqnsfile = fopen(filename, "r");
		i = 0;
		while(fscanf(seqnsfile, "%d ", &in)>0)
		{	X[i] = in;
			i++;
			if(i%l==0)
			{	i = 0;
				#if NUMSPLITS > 1
				if(splitcount%NUMSPLITS!=splitcase)
				{	splitcount++;
					continue;
				}
				splitcount++;
				#endif

				for(int j=0; j<l; j++)
					fft_signal[j] = X[j];
				fftw_execute(plan);
				for(int j=1; j<=l/2; j++)
					psds[j] = fft_result[j][0]*fft_result[j][0];

				Aseqns.push_back(X);
				Apsdslist.push_back(psds);
			}
		}
		fclose(seqnsfile);

		splitcount = 0;
		sprintf(filename, pafsfilename, n, c, l, "A");
		pafsfile = fopen(filename, "r");
		i = 0;
		while(fscanf(pafsfile, "%d ", &in)>0)
		{	P[i] = in;
			i++;
			if(i%pafslen==0)
			{	i = 0;
				#if NUMSPLITS > 1
				if(splitcount%NUMSPLITS!=splitcase)
				{	splitcount++;
					continue;
				}
				splitcount++;
				#endif
				Apafs.push_back(P);
			}
		}
		fclose(pafsfile);

		sprintf(filename, seqnsfilename, n, c, l, "B");
		seqnsfile = fopen(filename, "r");
		i = 0;
		while(fscanf(seqnsfile, "%d ", &in)>0)
		{	X[i] = in;
			i++;
			if(i%l==0)
			{	i = 0;

				for(int j=0; j<l; j++)
					fft_signal[j] = X[j];
				fftw_execute(plan);
				for(int j=1; j<=l/2; j++)
					psds[j] = fft_result[j][0]*fft_result[j][0];

				Bseqns.push_back(X);
				Bpsdslist.push_back(psds);
			}
		}
		fclose(seqnsfile);

		sprintf(filename, pafsfilename, n, c, l, "B");
		pafsfile = fopen(filename, "r");
		i = 0;
		while(fscanf(pafsfile, "%d ", &in)>0)
		{	P[i] = in;
			i++;
			if(i%pafslen==0)
			{	i = 0;
				Bpafs.push_back(P);
			}
		}
		fclose(pafsfile);
		#endif

		#if defined(CD) || defined(ABCD)
		sprintf(filename, seqnsfilename, n, c, l, "C");
		seqnsfile = fopen(filename, "r");
		i = 0;
		while(fscanf(seqnsfile, "%d ", &in)>0)
		{	X[i] = in;
			i++;
			if(i%l==0)
			{	i = 0;

				for(int j=0; j<l; j++)
					fft_signal[j] = X[j];
				fftw_execute(plan);
				for(int j=1; j<=l/2; j++)
					psds[j] = fft_result[j][0]*fft_result[j][0];

				Cseqns.push_back(X);
				Cpsdslist.push_back(psds);
			}
		}
		fclose(seqnsfile);

		sprintf(filename, pafsfilename, n, c, l, "C");
		pafsfile = fopen(filename, "r");
		i = 0;
		while(fscanf(pafsfile, "%d ", &in)>0)
		{	P[i] = in;
			i++;
			if(i%pafslen==0)
			{	i = 0;
				Cpafs.push_back(P);
			}
		}
		fclose(pafsfile);

		sprintf(filename, seqnsfilename, n, c, l, "D");
		seqnsfile = fopen(filename, "r");
		i = 0;
		while(fscanf(seqnsfile, "%d ", &in)>0)
		{	X[i] = in;
			i++;
			if(i%l==0)
			{	i = 0;

				for(int j=0; j<l; j++)
					fft_signal[j] = X[j];
				fftw_execute(plan);
				for(int j=1; j<=l/2; j++)
					psds[j] = fft_result[j][0]*fft_result[j][0];

				Dseqns.push_back(X);
				Dpsdslist.push_back(psds);
			}
		}
		fclose(seqnsfile);

		sprintf(filename, pafsfilename, n, c, l, "D");
		pafsfile = fopen(filename, "r");
		i = 0;
		while(fscanf(pafsfile, "%d ", &in)>0)
		{	P[i] = in;
			i++;
			if(i%pafslen==0)
			{	i = 0;
				Dpafs.push_back(P);
			}
		}
		fclose(pafsfile);
		#endif

		long ABcount = 0;
		long CDcount = 0;

		std::array<double, HALF_MAX_N> Apsds = {};
		std::array<double, HALF_MAX_N> Bpsds = {};
		std::array<double, HALF_MAX_N> ABpsds = {};
		std::array<double, HALF_MAX_N> Cpsds = {};
		std::array<double, HALF_MAX_N> Dpsds = {};
		std::array<double, HALF_MAX_N> CDpsds = {};

		FILE* pairfile;
		bool tobreak;

		#if defined(AB) || defined(ABCD)
		#if NUMSPLITS == 1
		sprintf(filename, pafsfilename, n, c, l, "AB");
		#else
		sprintf(filename, pairedpafsfilename, n, c, l, "AB", splitcase);
		#endif
		pairfile = fopen(filename, "w");

		for(int iA = 0; iA < Apsdslist.size(); iA++)
		{	
			Apsds = Apsdslist[iA];

			for(int iB = 0; iB < Bpsdslist.size(); iB++)
			{	
				Bpsds = Bpsdslist[iB];

				tobreak = false;
				for(int j=1; j<=l/2; j++)
				{	ABpsds[j] = Apsds[j]+Bpsds[j];
					if(ABpsds[j] > 4*n+0.01)
					{	tobreak = true;
						break;
					}
				}
				if(tobreak)
					continue;

				for(int i = 0; i < pafslen; i++)
					ABpafs[i] = Apafs[iA][i] + Bpafs[iB][i];

				#if NUMSPLITS == 1
				fprintpair(pairfile, pafslen, ABpafs.data(), iA, iB);
				#else
				fprintpair(pairfile, pafslen, ABpafs.data(), NUMSPLITS*iA+splitcase, iB);
				#endif
				ABcount++;
			}
		}

		fclose(pairfile);
		#endif

		#if defined(CD) || defined(ABCD)
		sprintf(filename, pafsfilename, n, c, l, "CD");
		pairfile = fopen(filename, "w");

		for(int iC = 0; iC < Cpsdslist.size(); iC++)
		{	
			Cpsds = Cpsdslist[iC];

			for(int iD = 0; iD < Dpsdslist.size(); iD++)
			{	
				Dpsds = Dpsdslist[iD];

				tobreak = false;
				for(int j=1; j<=l/2; j++)
				{	CDpsds[j] = Cpsds[j]+Dpsds[j];
					if(CDpsds[j] > 4*n+0.01)
					{	tobreak = true;
						break;
					}
				}
				if(tobreak)
					continue;

				for(int i = 0; i < pafslen; i++)
				{	CDpafs[i] = - (Cpafs[iC][i] + Dpafs[iD][i]);
					if(i==0)
						CDpafs[i] += 4*n;
				}

				fprintpair(pairfile, pafslen, CDpafs.data(), iC, iD);
				CDcount++;
			}
		}

		fclose(pairfile);
		#endif

		#if defined(NOCOMPRESSION)
		sprintf(filename, "timings/%d.%d.%d.genpairtimenocompress", n, c, l);
		#elif defined(AB) && NUMSPLITS>1
		sprintf(filename, "timings/%d.%d.%d.AB.%d.genpairtime", n, c, l, splitcase);
		#elif defined(AB)
		sprintf(filename, "timings/%d.%d.%d.AB.genpairtime", n, c, l);
		#elif defined(CD)
		sprintf(filename, "timings/%d.%d.%d.CD.genpairtime", n, c, l);
		#else
		sprintf(filename, "timings/%d.%d.%d.genpairtime", n, c, l);
		#endif
		FILE* f = fopen(filename, "w");
		fprintf(f, "%.2f\n", (clock() - start)/(float)CLOCKS_PER_SEC);
		fclose(f);

		printf("  Case %d: %ld AB and %ld CD paired PAF sequences of length %d generated in %.2f seconds\n", c, ABcount, CDcount, pafslen, (clock() - start)/(float)CLOCKS_PER_SEC);

	}

	fftw_destroy_plan(plan);
	free(fft_signal);
	free(fft_result);

}
