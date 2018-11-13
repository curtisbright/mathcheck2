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
#define REMOVE_EQUIV_A 1
#define REMOVE_EQUIV_B 0

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

double* fft_signal_A;
fftw_complex* fft_result_A;
fftw_plan plan_A;

double* fft_signal_B;
fftw_complex* fft_result_B;
fftw_plan plan_B;

int paf(int n, int* A, int s)
{	int res = 0;
	for(int i=0; i<n; i++)
		res += A[i]*A[(i+s)%n];
	return res;
}

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
		fprintf(f, "%d ", paf(n, A, i));
	}
	fprintf(f, "\n");
}

int main(int argc, char** argv)
{
	if(argc==1)
		fprintf(stderr, "Need order of matchings to compute\n"), exit(0);

	const int n = atoi(argv[1]);

	int d;
	if(argc>2)
		d = atoi(argv[2]);
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

	const char seqnsfilename[] = "matchings/%d.%d.%d.%c.seqns.txt";
	const char pafsfilename[] = "matchings/%d.%d.%d.%c.pafs.txt";

	mkdir("matchings", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
	mkdir("timings", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

	printf("ORDER %d: Generate compression sequences\n", n);

	fft_signal_A = (double*)malloc(sizeof(double)*n);
	fft_result_A = (fftw_complex*)malloc(sizeof(fftw_complex)*n);
	plan_A = fftw_plan_dft_r2c_1d(n, fft_signal_A, fft_result_A, FFTW_ESTIMATE);
	fft_signal_B = (double*)malloc(sizeof(double)*n);
	fft_result_B = (fftw_complex*)malloc(sizeof(fftw_complex)*n);
	plan_B = fftw_plan_dft_r2c_1d(n, fft_signal_B, fft_result_B, FFTW_ESTIMATE);

	FILE *Aseqnsfile, *Bseqnsfile[4], *Cseqnsfile[4], *Dseqnsfile[4];
	FILE *Apafsfile,  *Bpafsfile[4],  *Cpafsfile[4],  *Dpafsfile[4];
	int Btarget[4], Ctarget[4], Dtarget[4];
	
	char filename[100];
	sprintf(filename, seqnsfilename, n, 0, l, 'A');
	Aseqnsfile = fopen(filename, "w");
	sprintf(filename, pafsfilename, n, 0, l, 'A');
	Apafsfile = fopen(filename, "w");
	
	for(int c = 0; c < decomps_len[n]; c++)
	{
		sprintf(filename, seqnsfilename, n, c, l, 'B');
		Bseqnsfile[c] = fopen(filename, "w");
		sprintf(filename, seqnsfilename, n, c, l, 'C');
		Cseqnsfile[c] = fopen(filename, "w");
		sprintf(filename, seqnsfilename, n, c, l, 'D');
		Dseqnsfile[c] = fopen(filename, "w");
		sprintf(filename, pafsfilename, n, c, l, 'B');
		Bpafsfile[c] = fopen(filename, "w");
		sprintf(filename, pafsfilename, n, c, l, 'C');
		Cpafsfile[c] = fopen(filename, "w");
		sprintf(filename, pafsfilename, n, c, l, 'D');
		Dpafsfile[c] = fopen(filename, "w");

		Btarget[c] = decomps[n][c][1]*(decomps[n][c][1] % 4 == n % 4 ? 1 : -1);
		Ctarget[c] = decomps[n][c][2]*(decomps[n][c][2] % 4 == n % 4 ? 1 : -1);
		Dtarget[c] = decomps[n][c][3]*(decomps[n][c][3] % 4 == n % 4 ? 1 : -1);
	}

	clock_t start = clock();
	int Acount = 0, Bcount[4] = {}, Ccount[4] = {}, Dcount[4] = {};

	std::array<int, MAX_N> A = {};
	std::array<int, MAX_N> B = {};
	A[0] = 1;
	B[0] = 1;
	fft_signal_A[0] = 1;
	fft_signal_B[0] = 1;
	for(int i=1; i<=n/2; i++)
	{	A[i] = -1;
		B[i] = -1;
		fft_signal_A[i] = A[i];
		fft_signal_B[i] = B[i];
	}
	for(int i=n/2+1; i<n; i++)
	{	A[i] = 1;
		B[i] = -1;
		fft_signal_A[i] = A[i];
		fft_signal_B[i] = B[i];
	}

	int rowsum = -n+2;

	std::set<std::array<int, MAX_N>> myset_A;
	std::set<std::array<int, MAX_N>> myset_B;

	while(1)
	{	
		bool filtered_A = false;
		bool filtered_B = false;
		
		fftw_execute(plan_A);
		for(int i=0; i<=n/2; i++)
		{	double psd_A_i = fft_result_A[i][0]*fft_result_A[i][0] + fft_result_A[i][1]*fft_result_A[i][1];
			if(psd_A_i > 4*n + 0.01)
				filtered_A = true;
		}

		fftw_execute(plan_B);
		for(int i=0; i<=n/2; i++)
		{	double psd_B_i = fft_result_B[i][0]*fft_result_B[i][0] + fft_result_B[i][1]*fft_result_B[i][1];
			if(psd_B_i > 4*n + 0.01)
				filtered_B = true;
		}

		if(!filtered_A)
		{	
			std::array<int, MAX_N> compressA = compress(n, l, A);
			if(myset_A.count(compressA)==0)
			{	
				bool toadd_A = true;
				#if REMOVE_EQUIV_A
				for(int j=0; j<coprimelist_len[n] && toadd_A==true; j++)
				{	const int k = coprimelist[n][j];
					std::array<int, MAX_N> permutedcomp = permuteA(l, k, compressA);
					if(myset_A.count(permutedcomp)!=0)
						toadd_A = false;
				}
				#endif
				
				if(toadd_A == true)
				{	fprintseqn(Aseqnsfile, l, compressA.data());
					fprintpafs(Apafsfile, l, compressA.data());
					Acount++;
				}
				
				myset_A.insert(compressA);
			}
		}

		if(!filtered_B)
		{
			std::array<int, MAX_N> compressB = compress(n, l, B);
			if(myset_B.count(compressB)==0)
			{
				for(int c = 0; c < decomps_len[n]; c++)
				{

					if(rowsum == Btarget[c])
					{	
						bool toadd_B = true;
						#if REMOVE_EQUIV_B
						for(int j=0; j<coprimelist_len[n] && toadd_B==true; j++)
						{	const int k = coprimelist[n][j];
							std::array<int, MAX_N> permutedcomp = permuteA(l, k, compressB);
							if(myset_B.count(permutedcomp)!=0)
								toadd_B = false;
						}
						#endif

						if(toadd_B == true)
						{	fprintseqn(Bseqnsfile[c], l, compressB.data());
							fprintpafs(Bpafsfile[c], l, compressB.data());
							Bcount[c]++;
						}
					}
					if(rowsum == Ctarget[c])
					{	
						fprintseqn(Cseqnsfile[c], l, compressB.data());
						fprintpafs(Cpafsfile[c], l, compressB.data());
						Ccount[c]++;
					}
					if(rowsum == Dtarget[c])
					{	
						fprintseqn(Dseqnsfile[c], l, compressB.data());
						fprintpafs(Dpafsfile[c], l, compressB.data());
						Dcount[c]++;
					}
				}
				myset_B.insert(compressB);
			}
		}

		int i;
		for(i=n/2; i>=1; i--)
		{	B[i] += 2;
			rowsum += 2;
			fft_signal_A[i] = fft_signal_B[i] = A[i] = B[i];
			if(2*i<n)
			{	B[n-i] += 2;
				rowsum += 2;
				fft_signal_B[n-i] = B[n-i];
				fft_signal_A[n-i] = A[n-i] = -B[n-i];
			}
			if(B[i]==3)
			{	B[i] = -1;
				rowsum -= 4;
				fft_signal_A[i] = fft_signal_B[i] = A[i] = B[i];
				if(2*i<n)
				{	B[n-i] = -1;
					rowsum -= 4;
					fft_signal_B[n-i] = B[n-i];
					fft_signal_A[n-i] = A[n-i] = -B[n-i];
				}
			}
			else
				break;
		}
		if(i==0)
			break;
	}

	sprintf(filename, "timings/%d.%d.gencomptime", n, l);
	FILE* f = fopen(filename, "w");
	fprintf(f, "%.2f\n", (clock() - start)/(float)CLOCKS_PER_SEC);
	fclose(f);

	printf("  %d-compressed matchings of length %d generated in %.2f seconds\n", d, n/d, (clock() - start)/(float)CLOCKS_PER_SEC);
	for(int c=0; c<decomps_len[n]; c++)
		printf("    Case (%d, %d, %d): %d As, %d Bs, %d Cs, %d Ds\n", Btarget[c], Ctarget[c], Dtarget[c], Acount, Bcount[c], Ccount[c], Dcount[c]);

	fclose(Aseqnsfile);
	fclose(Apafsfile);

	for(int c=0; c<decomps_len[n]; c++)
	{	
		fclose(Bseqnsfile[c]);
		fclose(Cseqnsfile[c]);
		fclose(Dseqnsfile[c]);
		fclose(Bpafsfile[c]);
		fclose(Cpafsfile[c]);
		fclose(Dpafsfile[c]);
	}

	fftw_destroy_plan(plan_A);
	free(fft_signal_A);
	free(fft_result_A);
	fftw_destroy_plan(plan_B);
	free(fft_signal_B);
	free(fft_result_B);

}
