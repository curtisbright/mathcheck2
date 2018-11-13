#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>
#include <fftw3.h>
#include <sys/types.h>
#include <sys/stat.h>
#include "decomps.h"

#if !defined(AB) && !defined(CD)
#define ABCD
#endif

const int MAX_N = 70;
const int HALF_MAX_N = 1+MAX_N/2;
#include <array>
#include <vector>

void fprintpair(FILE* f, int n, int* A, int iA, int iB)
{	for(int i=0; i<n; i++)
		fprintf(f, "%d ", A[i]);
	fprintf(f, ": %d %d\n", iA, iB);
}

int main(int argc, char** argv)
{
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
		else if(n%7 == 0)
			d = 7;
		else
			d = 1;
	}
	const int l = n/d;

	const char seqnsfilename[] = "matchings/%d.%d.%d.%s.seqns.txt";
	const char pafsfilename[] = "matchings/%d.%d.%d.%s.pafs.txt";

	mkdir("timings", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

	const int pafslen = l/2+1;

	printf("ORDER %d: Generate compression sequence pairs\n", n);

	double* fft_signal = (double*)malloc(sizeof(double)*l);
	fftw_complex* fft_result = (fftw_complex*)malloc(sizeof(fftw_complex)*l);
	fftw_plan plan = fftw_plan_dft_r2c_1d(l, fft_signal, fft_result, FFTW_ESTIMATE);

	char filename[100];
	FILE* seqnsfile;
	FILE* pafsfile;

	std::vector<std::array<int, MAX_N>> Aseqns;
	std::vector<std::array<int, HALF_MAX_N>> Apafs;
	std::vector<std::array<double, HALF_MAX_N>> Apsdslist;
	std::array<int, MAX_N> X = {};
	std::array<int, HALF_MAX_N> P = {};
	std::array<double, HALF_MAX_N> psds = {};

	int in, i;
	#if defined(AB) || defined(ABCD)
	clock_t start = clock();
	int splitcount = 0;

	sprintf(filename, seqnsfilename, n, 0, l, "A");
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
				psds[j] = fft_result[j][0]*fft_result[j][0]+fft_result[j][1]*fft_result[j][1];

			Aseqns.push_back(X);
			Apsdslist.push_back(psds);
		}
	}
	fclose(seqnsfile);

	splitcount = 0;
	sprintf(filename, pafsfilename, n, 0, l, "A");
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
	printf("  Computed A PSDs in %.2f seconds\n", (clock() - start)/(float)CLOCKS_PER_SEC);
	#endif

	for(int c = 0; c < decomps_len[n]; c++)
	{
		if(casetosolve != -1 && casetosolve != c)
			continue;
			
		std::vector<std::array<int, MAX_N>> Bseqns;
		std::vector<std::array<int, MAX_N>> Cseqns;
		std::vector<std::array<int, MAX_N>> Dseqns;
		std::vector<std::array<double, HALF_MAX_N>> Bpsdslist;
		std::vector<std::array<double, HALF_MAX_N>> Cpsdslist;
		std::vector<std::array<double, HALF_MAX_N>> Dpsdslist;
		std::vector<std::array<int, HALF_MAX_N>> Bpafs;
		std::vector<std::array<int, HALF_MAX_N>> Cpafs;
		std::vector<std::array<int, HALF_MAX_N>> Dpafs;

		std::array<int, HALF_MAX_N> ABpafs;
		std::array<int, HALF_MAX_N> CDpafs;

		clock_t start = clock();
		#if defined(AB) || defined(ABCD)
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
				{	psds[j] = fft_result[j][0]*fft_result[j][0];
				}

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
				{	psds[j] = fft_result[j][0]*fft_result[j][0];
				}

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
				{	psds[j] = fft_result[j][0]*fft_result[j][0];
				}

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
		sprintf(filename, pafsfilename, n, c, l, "AB");
		pairfile = fopen(filename, "w");

		for(int iA = 0; iA < Apsdslist.size(); iA++)
		{	
			if(decomps[n][c][0]*decomps[n][c][0]+decomps[n][c][1]*decomps[n][c][1]+decomps[n][c][2]*decomps[n][c][2] == 4*n && Aseqns[iA][0] != 0)
				continue;
			if(decomps[n][c][0]*decomps[n][c][0]+decomps[n][c][1]*decomps[n][c][1]+decomps[n][c][2]*decomps[n][c][2] == 4*n-2 && Aseqns[iA][0] == 0)
				continue;

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

				fprintpair(pairfile, pafslen, ABpafs.data(), iA, iB);
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

		sprintf(filename, "timings/%d.%d.%d.genpairtime", n, c, l);
		FILE* f = fopen(filename, "w");
		fprintf(f, "%.2f\n", (clock() - start)/(float)CLOCKS_PER_SEC);
		fclose(f);

		printf("  Case %d: %ld AB and %ld CD paired PAF sequences of length %d generated in %.2f seconds\n", c, ABcount, CDcount, pafslen, (clock() - start)/(float)CLOCKS_PER_SEC);

	}

	fftw_destroy_plan(plan);
	free(fft_signal);
	free(fft_result);

}
