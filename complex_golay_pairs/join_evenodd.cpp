#include <math.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <fftw3.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <array>
#include <vector>

#define NC 128
#define NUMSPLITS 1
#define MAX_SIZE N

const int nchecks = NC;
const int n = N;
const int splits = NUMSPLITS;

#include "squaredecompfilter.h"

std::vector<std::array<fftw_complex, MAX_SIZE>> odds;
std::vector<std::array<fftw_complex, NC>> odds_dft;

fftw_complex* in;
fftw_complex* out;
fftw_plan p;

void fprint_join(FILE* f, const fftw_complex* evens, const std::array<fftw_complex, MAX_SIZE>& odds)
{	for(int k=0; k<n; k++)
	{	if(k%2==0)
		{	if(evens[k][0]==1 && evens[k][1]==0)
				fprintf(f, "+");
			else if(evens[k][0]==-1 && evens[k][1]==0)
				fprintf(f, "-");
			else if(evens[k][0]==0 && evens[k][1]==1)
				fprintf(f, "i");
			else if(evens[k][0]==0 && evens[k][1]==-1)
				fprintf(f, "j");
			else if(evens[k][0]==0 && evens[k][1]==0)
				fprintf(f, "*");
		}
		else
		{	if(odds[k][0]==1 && odds[k][1]==0)
				fprintf(f, "+");
			else if(odds[k][0]==-1 && odds[k][1]==0)
				fprintf(f, "-");
			else if(odds[k][0]==0 && odds[k][1]==1)
				fprintf(f, "i");
			else if(odds[k][0]==0 && odds[k][1]==-1)
				fprintf(f, "j");
			else if(odds[k][0]==0 && odds[k][1]==0)
				fprintf(f, "*");
		}
	}
	fprintf(f, "\n");
}

const int samples_order[NC-4] = {16, 48, 80, 112, 8, 24, 40, 56, 72, 88, 104, 120, 4, 12, 20, 28, 36, 44, 52, 60, 68, 76, 84, 92, 100, 108, 116, 124, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 118, 122, 126, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127};

bool hall_pass_filter(const fftw_complex* evens_dft, const std::array<fftw_complex, NC>& odds_dft)
{	
	for(int l=0; l<NC-4; l++)
	{		
		const int k = samples_order[l];
		const double rdft = evens_dft[k][0] + odds_dft[k][0];
		const double idft = evens_dft[k][1] + odds_dft[k][1];
		const double psd = rdft*rdft+idft*idft;
		
		if(psd - 2*n > 0.001)
		{	
			return true;
		}
	}
	
	return false;
}

int main(int argc, char** argv)
{	
	char filename[100];
	clock_t start = clock();

	const char strfilenameeven[] = "leftovers/leftover.%d.even.txt";
	const char strfilenameodd[] = "leftovers/leftover.%d.%d.odd.txt";
	const char strfilenamejoin[] = "joins/join.%d.%d.txt";
	const char timingsname[] = "timings/%d.%d.join.time";
	mkdir("joins", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
	mkdir("timings", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

	in = fftw_alloc_complex(nchecks);
	out = fftw_alloc_complex(nchecks);
	p = fftw_plan_dft_1d(nchecks, in, out, FFTW_BACKWARD, FFTW_ESTIMATE);

	long totalfail = 0;
	long totalsuccess = 0;
	long totalcount = 0;

	odds.clear();
	odds_dft.clear();

	for(int i=0; i<nchecks; i++)
	{	in[i][0] = 0, in[i][1] = 0;
	}

	sprintf(filename, strfilenameeven, n);
	FILE* f = fopen(filename, "r");
	if(f == NULL)
		fprintf(stderr, "File %s not opened.\n", filename), exit(0);

	int splitsnum = 0;
	if(argc>=2)
		splitsnum = atoi(argv[1]);

	sprintf(filename, strfilenameodd, n, splitsnum);
	FILE* g = fopen(filename, "r");
	if(g == NULL)
		fprintf(stderr, "File %s not opened.\n", filename), exit(0);

	std::array<fftw_complex, MAX_SIZE> B = {};
	int c = 0;
	int i = 0;
	while(c != EOF)
	{	
		c = fgetc(g);
		if(c=='+')
		{	B[i][0] = 1, B[i][1] = 0;
			in[i][0] = 1, in[i][1] = 0;
		}
		else if(c=='-')
		{	B[i][0] = -1, B[i][1] = 0;
			in[i][0] = -1, in[i][1] = 0;
		}
		else if(c=='i')
		{	B[i][0] = 0, B[i][1] = 1;
			in[i][0] = 0, in[i][1] = 1;
		}
		else if(c=='j')
		{	B[i][0] = 0, B[i][1] = -1;
			in[i][0] = 0, in[i][1] = -1;
		}
		else if(c=='\n')
		{	i = -1;
			odds.push_back(B);
			fftw_execute(p);
			std::array<fftw_complex, NC> B_dft;
			for(int k=0; k<nchecks; k++)
			{	B_dft[k][0] = out[k][0], B_dft[k][1] = out[k][1];
			}
			odds_dft.push_back(B_dft);
		}
		i++;
	}
	
	fclose(g);

	for(int i=0; i<nchecks; i++)
	{	in[i][0] = 0, in[i][1] = 0;
	}
	
	sprintf(filename, strfilenamejoin, n, splitsnum);
	FILE* h = fopen(filename, "w");
	if(h == NULL)
		fprintf(stderr, "File %s not opened.\n", filename), exit(0);

	const int odds_size = odds.size();
	
	c = 0;
	i = 0;
	while(c != EOF)
	{	c = fgetc(f);
		if(c=='+')
			in[i][0] = 1, in[i][1] = 0;
		else if(c=='-')
			in[i][0] = -1, in[i][1] = 0;
		else if(c=='i')
			in[i][0] = 0, in[i][1] = 1;
		else if(c=='j')
			in[i][0] = 0, in[i][1] = -1;
		else if(c=='\n')
		{	i = -1;
			fftw_execute(p);

			for(int j=0; j<odds_size; j++)
			{
				if(!square_decomp_filter(out, odds_dft[j]) && !hall_pass_filter(out, odds_dft[j]))
				{	totalfail++;
					fprint_join(h, in, odds[j]);
				}
				else
				{	totalsuccess++;
				}
				
				totalcount++;
			}
		}
		i++;
	}
	
	fclose(f);
	fclose(h);

	fftw_destroy_plan(p);
	fftw_free(out);
	fftw_free(in);
	
	clock_t end = clock();

	sprintf(filename, timingsname, n, splitsnum);
	f = fopen(filename, "w");
	fprintf(f, "%.2f\n", (end-start)/(float)CLOCKS_PER_SEC);
	fclose(f);

	if(splits==1)
		printf("Order %d time: %.2f seconds, total: %ld, leftover: %ld (%.5Lf%%), filtered: %ld (%.5Lf%%)\n", n, (end-start)/(float)CLOCKS_PER_SEC, totalcount, totalfail, 100*totalfail/(long double)totalcount, totalsuccess, 100*(totalsuccess/(long double)totalcount));
	else
		printf("Order %d split %d time: %.2f seconds, total: %ld, leftover: %ld (%.5Lf%%), filtered: %ld (%.5Lf%%)\n", n, splitsnum, (end-start)/(float)CLOCKS_PER_SEC, totalcount, totalfail, 100*totalfail/(long double)totalcount, totalsuccess, 100*(totalsuccess/(long double)totalcount));

	return 0;
}
