#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>
#include <fftw3.h>
#include <sys/types.h>
#include <sys/stat.h>
#include "decomps.h"

#include <array>
#include <set>
#include "coprimelist.h"
#define MAX_N 70

std::array<int, MAX_N> compress(int n, int l, std::array<int, MAX_N> A)
{	
	std::array<int, MAX_N> result = {};
	for(int i=0; i<n; i++)
	{	result[i%l] += A[i];
	}
	return result;
}

std::array<int, MAX_N> permuteA(int n, int k, std::array<int, MAX_N> A)
{	std::array<int, MAX_N> result = {};
	for(int i=0; i<n; i++)
	{	result[i] = A[(i*k)%n];
	}
	return result;
}

#define ASSERT 0
#ifndef DEBUG
#define DEBUG 0
#endif
#define FFTWPAFS 0

#if ASSERT==1
#include <assert.h>
#endif

#if ASSERT==1 || FFTWPAFS==1
#include <math.h>
#endif

double* fft_signal;
fftw_complex* fft_result;
fftw_plan plan;

#if ASSERT==1 || FFTWPAFS==1
fftw_complex* fft_signal_2;
double* fft_result_2;
fftw_plan plan_2;
#endif

#if ASSERT==1 || FFTWPAFS==0
int paf(int n, int* A, int s)
{	int res = 0;
	for(int i=0; i<n; i++)
		res += A[i]*A[(i+s)%n];
	return res;
}
#endif

#if DEBUG==1
void printA(int n, int* A, double* psds, int rowsum)
{	for(int i=0; i<n; i++)
		printf("%d ", A[i]);
	printf(": ");
	#if ASSERT==1 || FFTWPAFS==0
	for(int i=0; i<n; i++)
		printf("%d ", paf(n, A, i));
	printf(": ");
	#endif
	for(int i=0; i<=n/2; i++)
		printf("%.2f ", psds[i]);
	printf(": ");
	#if ASSERT==1 || FFTWPAFS==1
	for(int i=0; i<n; i++)
		printf("%ld ", lround(fft_result_2[i]/n));
	printf(": ");
	#endif
	printf("%d", rowsum);
	printf("\n");
}
#endif

void fprintseqn(FILE* f, int n, int* A)
{	
	for(int i=0; i<n; i++)
		fprintf(f, "%d ", A[i]);
	fprintf(f, "\n");
}

void fprintpafs(FILE* f, int n, int* A)
{	
	for(int i=0; i<=n/2; i++)
	{
		#if FFTWPAFS==1
		fprintf(f, "%ld ", lround(fft_result_2[i]/n));
		#else
		fprintf(f, "%d ", paf(n, A, i));
		#endif
		#if ASSERT==1
		assert(paf(n, A, i) == lround(fft_result_2[i]/n));
		#endif
	}
	fprintf(f, "\n");
}

int main(int argc, char** argv)
{
	char filename[100];
	int n1, n2;

	if(argc==1)
		fprintf(stderr, "Need order of matchings to compute\n"), exit(0);

	const int n = atoi(argv[1]);

	bool remove_equiv_d = true;
	int d;
	if(argc>2)
	{	d = atoi(argv[2]);
		remove_equiv_d = false;
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

	const char seqnsfilename[] = "matchings/%d.%d.%d.%c.seqns.txt";
	const char pafsfilename[] = "matchings/%d.%d.%d.%c.pafs.txt";

	mkdir("matchings", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
	mkdir("timings", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

	printf("ORDER %d: Generate compression sequences\n", n);

	fft_signal = (double*)malloc(sizeof(double)*n);
	fft_result = (fftw_complex*)malloc(sizeof(fftw_complex)*n);
	plan = fftw_plan_dft_r2c_1d(n, fft_signal, fft_result, FFTW_ESTIMATE);

	#if ASSERT==1 || FFTWPAFS==1
	fft_signal_2 = (fftw_complex*)malloc(sizeof(fftw_complex)*n);
	for(int i=0; i<n; i++)
		fft_signal_2[i][1] = 0;
	fft_result_2 = (double*)malloc(sizeof(double)*n);
	plan_2 = fftw_plan_dft_c2r_1d(n, fft_signal_2, fft_result_2, FFTW_ESTIMATE | FFTW_PRESERVE_INPUT);
	#endif

	FILE *Aseqnsfile[8], *Bseqnsfile[8], *Cseqnsfile[8], *Dseqnsfile[8];
	FILE *Apafsfile[8],  *Bpafsfile[8],  *Cpafsfile[8],  *Dpafsfile[8];
	
	for(int c = 0; c < decomps_len[n]; c++)
	{
		char filename[100];
		sprintf(filename, seqnsfilename, n, c, l, 'A');
		Aseqnsfile[c] = fopen(filename, "w");
		sprintf(filename, seqnsfilename, n, c, l, 'B');
		Bseqnsfile[c] = fopen(filename, "w");
		sprintf(filename, seqnsfilename, n, c, l, 'C');
		Cseqnsfile[c] = fopen(filename, "w");
		sprintf(filename, seqnsfilename, n, c, l, 'D');
		Dseqnsfile[c] = fopen(filename, "w");
		sprintf(filename, pafsfilename, n, c, l, 'A');
		Apafsfile[c] = fopen(filename, "w");
		sprintf(filename, pafsfilename, n, c, l, 'B');
		Bpafsfile[c] = fopen(filename, "w");
		sprintf(filename, pafsfilename, n, c, l, 'C');
		Cpafsfile[c] = fopen(filename, "w");
		sprintf(filename, pafsfilename, n, c, l, 'D');
		Dpafsfile[c] = fopen(filename, "w");
	}

	clock_t start = clock();
	int Acount[8] = {}, Bcount[8] = {}, Ccount[8] = {}, Dcount[8] = {};

	//int A[n];
	std::array<int, MAX_N> A = {};
	for(int i=0; i<n; i++)
	{	A[i] = -1;
		fft_signal[i] = A[i];
	}

	int rowsum = -n;

	std::set<std::array<int, MAX_N>> myset;

	while(1)
	{	
		bool filtered = false;
		
		#if DEBUG==1
		double psds[n/2+1];
		#endif
		
		if(rowsum == 0 && A[0] == -1)
			filtered = true;
		else
		{
			fftw_execute(plan);

			for(int i=0; i<=n/2; i++)
			{	double psd_i = fft_result[i][0]*fft_result[i][0];
				#if DEBUG==1
				psds[i] = psd_i;
				#endif
				#if ASSERT==1 || FFTWPAFS==1
				fft_signal_2[i][0] = psd_i;
				#endif
				if(psd_i > 4*n + 0.01)
				{	filtered = true;
					#if DEBUG==0
					break;
					#endif
				}
			}
		}

		if(!filtered)
		{
			#if ASSERT==1 || FFTWPAFS==1
			fftw_execute(plan_2);
			#endif

			#if DEBUG==1
			printA(n, A.data(), psds, rowsum);
			#endif
			
			std::array<int, MAX_N> compressA = compress(n, l, A);
			if(myset.count(compressA)==0)
			{
				for(int c = 0; c < decomps_len[n]; c++)
				{
					int Atarget = decomps[n][c][0]*(decomps[n][c][0] % 4 == 3 ? -1 : 1);
					int Btarget = decomps[n][c][1]*(decomps[n][c][1] % 4 == 3 ? -1 : 1);
					int Ctarget = decomps[n][c][2]*(decomps[n][c][2] % 4 == 3 ? -1 : 1);
					int Dtarget = decomps[n][c][3]*(decomps[n][c][3] % 4 == 3 ? -1 : 1);
						
					bool toadd_D = true;
				
					if(remove_equiv_d)
					{	for(int j=0; j<=coprimelength[n] && toadd_D==true; j++)
						{	const int k = coprimelist[n][j];
							std::array<int, MAX_N> permutedcomp = permuteA(l, k, compressA);
							if(myset.count(permutedcomp)!=0)
								toadd_D = false;
						}
					}

					if(rowsum == Atarget)
					{	
						fprintseqn(Aseqnsfile[c], l, compressA.data());
						fprintpafs(Apafsfile[c], l, compressA.data());
						Acount[c]++;
					}
					if(rowsum == Btarget)
					{	
						fprintseqn(Bseqnsfile[c], l, compressA.data());
						fprintpafs(Bpafsfile[c], l, compressA.data());
						Bcount[c]++;
					}
					if(rowsum == Ctarget)
					{	
						fprintseqn(Cseqnsfile[c], l, compressA.data());
						fprintpafs(Cpafsfile[c], l, compressA.data());
						Ccount[c]++;
					}
					if(rowsum == Dtarget && toadd_D)
					{	
						fprintseqn(Dseqnsfile[c], l, compressA.data());
						fprintpafs(Dpafsfile[c], l, compressA.data());
						Dcount[c]++;
					}
				}
				myset.insert(compressA);
			}
		}

		int i;
		for(i=n/2; i>=0; i--)
		{	A[i] += 2;
			rowsum += 2;
			fft_signal[i] = A[i];
			if(i>0 && 2*i<n)
			{	A[n-i] += 2;
				rowsum += 2;
				fft_signal[n-i] = A[n-i];
			}
			if(A[i]==3)
			{	A[i] = -1;
				rowsum -= 4;
				fft_signal[i] = A[i];
				if(i>0 && 2*i<n)
				{	A[n-i] = -1;
					rowsum -= 4;
					fft_signal[n-i] = A[n-i];
				}
			}
			else
				break;
		}
		if(i==-1)
			break;
	}

	sprintf(filename, "timings/%d.%d.gencomptime", n, l);
	FILE* f = fopen(filename, "w");
	fprintf(f, "%.2f\n", (clock() - start)/(float)CLOCKS_PER_SEC);
	fclose(f);

	printf("  %d-compressed matchings of length %d generated in %.2f seconds\n", d, n/d, (clock() - start)/(float)CLOCKS_PER_SEC);
	for(int i=0; i<decomps_len[n]; i++)
		printf("    Case %d: %d As, %d Bs, %d Cs, %d Ds\n", i, Acount[i], Bcount[i], Ccount[i], Dcount[i]);

	for(int c=0; c<decomps_len[n]; c++)
	{	fclose(Aseqnsfile[c]);
		fclose(Bseqnsfile[c]);
		fclose(Cseqnsfile[c]);
		fclose(Dseqnsfile[c]);
		fclose(Apafsfile[c]);
		fclose(Bpafsfile[c]);
		fclose(Cpafsfile[c]);
		fclose(Dpafsfile[c]);
	}

	fftw_destroy_plan(plan);
	free(fft_signal);
	free(fft_result);

	#if ASSERT==1 || FFTWPAFS==1
	fftw_destroy_plan(plan_2);
	free(fft_signal_2);
	free(fft_result_2);
	#endif

}
