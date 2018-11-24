#include <math.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <complex.h>
#include <fftw3.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <array>
#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <algorithm>
#include <utility>

#define MAX_SIZE N
#define NC 32

const int nchecks = NC;
const int n = N;

#include "squaredecompfilter.h"

std::vector<std::array<fftwf_complex, NC>> odds_dft;
std::vector<std::array<int, 5>> odds_rowsum;

std::vector<std::array<fftwf_complex, NC>> evens_dft;
std::vector<std::array<int, 5>> evens_rowsum;

fftwf_complex* in;
fftwf_complex* out;
fftwf_plan p;

#if NC==16
const int samples_order[NC-4] = {2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15};
#elif NC==32
const int samples_order[NC-4] = {4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31};
#elif NC==64
const int samples_order[NC-4] = {8, 24, 40, 56, 4, 12, 20, 28, 36, 44, 52, 60, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63};
#elif NC==128
const int samples_order[NC-4] = {16, 48, 80, 112, 8, 24, 40, 56, 72, 88, 104, 120, 4, 12, 20, 28, 36, 44, 52, 60, 68, 76, 84, 92, 100, 108, 116, 124, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 118, 122, 126, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127};
#endif

bool hall_pass_filter(const std::array<fftwf_complex, NC>& evens_dft, const std::array<fftwf_complex, NC>& odds_dft)
{	
	for(int l=0; l<NC-4; l++)
	{		
		const int k = samples_order[l];
		const float rdft = evens_dft[k][0] + odds_dft[k][0];
		const float idft = evens_dft[k][1] + odds_dft[k][1];
		const float psd = rdft*rdft+idft*idft;
		
		if(psd - 2*n > 0.001)
			return true;
	}

	return false;
}

// Compare rowsum vectors using shifts (u_0, u_1, u_2, u_3)
int compare_rowsums(const std::array<int, 5>& x, const std::array<int, 5>& y, int k, int l)
{
	if(x[0]<decomps[n][k][0]+y[0])
		return 2;

	if(x[0]>decomps[n][k][0]+y[0])
		return -2;

	if(x[1]<decomps[n][k][1]+y[1])
		return 2;

	if(x[1]>decomps[n][k][1]+y[1])
		return -2;

	if(x[2]<decomps[n][l][0]+y[2])
		return 1;

	if(x[2]>decomps[n][l][0]+y[2])
		return -1;

	if(x[3]<decomps[n][l][1]+y[3])
		return 1;

	if(x[3]>decomps[n][l][1]+y[3])
		return -1;

	return 0;
}

// Compare first two coordinates of rowsum vectors using shift (u_0, u_1)
int compare_rowsums(const std::array<int, 5>& x, const std::array<int, 5>& y, int k)
{
	if(x[0]<decomps[n][k][0]+y[0])
		return 2;

	if(x[0]>decomps[n][k][0]+y[0])
		return -2;

	if(x[1]<decomps[n][k][1]+y[1])
		return 2;

	if(x[1]>decomps[n][k][1]+y[1])
		return -2;

	return 0;
}

// Compare rowsum vectors with no shifts
int compare_rowsums(const std::array<int, 5>& x, const std::array<int, 5>& y)
{
	if(x[0]<y[0])
		return 1;

	if(x[0]>y[0])
		return -1;

	if(x[1]<y[1])
		return 1;

	if(x[1]>y[1])
		return -1;

	if(x[2]<y[2])
		return 1;

	if(x[2]>y[2])
		return -1;

	if(x[3]<y[3])
		return 1;

	if(x[3]>y[3])
		return -1;

	return 0;
}

int main(int argc, char** argv)
{	
	char filename[100];
	clock_t start = clock();

	const char strfilenameeven[] = "leftovers/leftover.%d.even.txt";
	const char strfilenameodd[] = "leftovers/leftover.%d.%d.odd.txt";
	const char strfilenamejoins[] = "joinsums/joinsums.%d.%d.txt";
	const char timingsname[] = "timings/%d.%d.joinsums.time";
	mkdir("joinsums", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
	mkdir("timings", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

	std::string str;

	in = fftwf_alloc_complex(nchecks);
	out = fftwf_alloc_complex(nchecks);
	p = fftwf_plan_dft_1d(nchecks, in, out, FFTW_BACKWARD, FFTW_ESTIMATE);

	odds_dft.clear();
	evens_dft.clear();

	for(int i=0; i<nchecks; i++)
	{	in[i][0] = 0, in[i][1] = 0;
	}

	sprintf(filename, strfilenameeven, n);
	FILE* f = fopen(filename, "r");
	if(f == NULL)
		fprintf(stderr, "File %s not opened.\n", filename), exit(0);

	int c = 0;
	int i = 0;
	while(c != EOF)
	{	
		c = fgetc(f);
		if(c=='+')
		{	in[i%NC][0] += 1;
		}
		else if(c=='-')
		{	in[i%NC][0] += -1;
		}
		else if(c=='i')
		{	in[i%NC][1] += 1;
		}
		else if(c=='j')
		{	in[i%NC][1] += -1;
		}
		else if(c=='\n')
		{	i = -1;
			fftwf_execute(p);
			std::array<fftwf_complex, NC> A_dft;
			for(int k=0; k<nchecks; k++)
			{	A_dft[k][0] = out[k][0], A_dft[k][1] = out[k][1];
			}

			for(int i=0; i<nchecks; i++)
			{	in[i][0] = 0, in[i][1] = 0;
			}

			evens_dft.push_back(A_dft);
		}
		i++;
	}
	
	fclose(f);

	int splitsnum = 0;
	if(argc>=2)
		splitsnum = atoi(argv[1]);

	sprintf(filename, strfilenameodd, n, splitsnum);
	FILE* g = fopen(filename, "r");
	if(g == NULL)
		fprintf(stderr, "File %s not opened.\n", filename), exit(0);

	for(int i=0; i<nchecks; i++)
	{	in[i][0] = 0, in[i][1] = 0;
	}

	c = 0;
	i = 0;
	while(c != EOF)
	{	
		c = fgetc(g);
		if(c=='+')
		{	in[i%NC][0] += 1;
		}
		else if(c=='-')
		{	in[i%NC][0] += -1;
		}
		else if(c=='i')
		{	in[i%NC][1] += 1;
		}
		else if(c=='j')
		{	in[i%NC][1] += -1;
		}
		else if(c=='\n')
		{	i = -1;
			fftwf_execute(p);
			std::array<fftwf_complex, NC> B_dft;
			for(int k=0; k<nchecks; k++)
			{	B_dft[k][0] = out[k][0], B_dft[k][1] = out[k][1];
			}

			for(int i=0; i<nchecks; i++)
			{	in[i][0] = 0, in[i][1] = 0;
			}

			odds_dft.push_back(B_dft);
		}
		i++;
	}
	
	fclose(g);

	fftwf_destroy_plan(p);
	fftwf_free(out);
	fftwf_free(in);

	const int evens_size = evens_dft.size();
	const int odds_size = odds_dft.size();

	sprintf(filename, strfilenamejoins, n, splitsnum);
	FILE* h = fopen(filename, "w");
	if(h == NULL)
		fprintf(stderr, "File %s not opened.\n", filename), exit(0);

	evens_rowsum.clear();
	odds_rowsum.clear();

	for(int i=0; i<evens_size; i++)
	{	std::array<int, 5> rowsums;
		rowsums[0] = evens_dft[i][0][0];
		rowsums[1] = evens_dft[i][0][1];
		rowsums[2] = roundf(evens_dft[i][NC/4][0]);
		rowsums[3] = roundf(evens_dft[i][NC/4][1]);
		rowsums[4] = i;
		evens_rowsum.push_back(rowsums);
	}

	for(int i=0; i<odds_size; i++)
	{	std::array<int, 5> rowsums;
		rowsums[0] = -odds_dft[i][0][0];
		rowsums[1] = -odds_dft[i][0][1];
		rowsums[2] = -roundf(odds_dft[i][NC/4][0]);
		rowsums[3] = -roundf(odds_dft[i][NC/4][1]);
		rowsums[4] = i;
		odds_rowsum.push_back(rowsums);
	}

	std::sort(evens_rowsum.begin(), evens_rowsum.end());
	std::sort(odds_rowsum.begin(), odds_rowsum.end());

	long num_matches = 0;
	long total = 0;

	//printf("  Initialization in %.2f seconds\n", (clock() - start)/(float)CLOCKS_PER_SEC);

	// (u_0, u_1) = (decomps[n][k][0], decomps[n][k][1])
	for(int k=0; k<decomps_len[n]; k++)
	{	
		int E_count_main = 0;
		int O_count_main = 0;
		int E_count = 0;
		int O_count = 0;

		while(E_count < evens_size && O_count < odds_size)
		{

			E_count_main = E_count;
			O_count_main = O_count;

			while(E_count_main < evens_size && O_count_main < odds_size)
			{
				const int compare_main = compare_rowsums(evens_rowsum[E_count_main], odds_rowsum[O_count_main], k);

				if(compare_main==2)
				{
					E_count_main++;
				}
				else if(compare_main==-2)
				{
					O_count_main++;
				}
				else
					break;
			}

			// (u_2, u_3) = (decomps[n][l][0], decomps[n][l][1])
			for(int l=0; l<decomps_len[n]; l++)
			{	
				E_count = E_count_main;
				O_count = O_count_main;

				while(E_count < evens_size && O_count < odds_size)
				{
					const int compare = compare_rowsums(evens_rowsum[E_count], odds_rowsum[O_count], k, l);

					if(compare==0)
					{	
						const int E_index = evens_rowsum[E_count][4];
						const int O_index = odds_rowsum[O_count][4];
						
						if(!square_decomp_filter(evens_dft[E_index], odds_dft[O_index]) && !hall_pass_filter(evens_dft[E_index], odds_dft[O_index]))
						{	fprintf(h, "%d %d\n", E_index, O_index);
							num_matches++;
						}
						total++;

						if(E_count==evens_size-1)
							O_count++;
						else
						{	if(O_count != odds_size-1 && compare_rowsums(odds_rowsum[O_count], odds_rowsum[O_count+1])==0)
								O_count++;
							else
							{	E_count++;
								while(O_count > 0 && compare_rowsums(odds_rowsum[O_count-1], odds_rowsum[O_count])==0)
									O_count--;
							}
						}
					}
					else if(compare==1)
					{
						E_count++;
					}
					else if(compare==-1)
					{
						O_count++;
					}
					else if(compare==2)
					{
						E_count++;
						break;
					}
					else if(compare==-2)
					{
						O_count++;
						break;
					}
				}
			}
		}
	}

	fclose(h);

	sprintf(filename, timingsname, n, splitsnum);
	h = fopen(filename, "w");
	fprintf(h, "%.2f\n", (clock() - start)/(float)CLOCKS_PER_SEC);
	fclose(h);

	printf("  %ld/%ld (filtered %.5f%%) matched sums generated in %.2f seconds\n", num_matches, total, 100*(1-num_matches/(double)total), (clock() - start)/(float)CLOCKS_PER_SEC);

	return 0;
}
