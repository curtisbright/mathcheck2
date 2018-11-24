#include <math.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <complex.h>
#include <fftw3.h>
#include <sys/types.h>
#include <sys/stat.h>

#define NC 16384
#define NUMSPLITS 1

fftw_complex* in;
fftw_complex* out;
fftw_plan p1, p2;

const int nchecks = NC;
const int n = N;
const int splits = NUMSPLITS;

void fprint_in(FILE* f)
{	for(int i=0; i<n; i++)
	{	if(in[i]==1)
			fprintf(f, "+");
		if(in[i]==-1)
			fprintf(f, "-");
		if(in[i]==I)
			fprintf(f, "i");
		if(in[i]==-I)
			fprintf(f, "j");
		if(in[i]==0)
			fprintf(f, "*");
	}
	fprintf(f, "\n");
}

bool hall_pass_filter_fftw(const fftw_plan* p, int const len)
{	
	fftw_execute(*p);

	for(int k=0; k<len; k++)
	{	const double rout = creal(out[k]);
		const double iout = cimag(out[k]);
		const double psd = rout*rout+iout*iout;

		if(psd - 2*n > 0.001)
			return true;
	}

	return false;
}

bool next_arr_even()
{	
	for(int k=4; k<n; k+=2)
	{	in[k] *= I;
		if(in[k]!=1)
			return true;
	}

	return false;
}

bool next_arr_odd()
{	
	for(int k=3; k<n; k+=2)
	{	in[k] *= I;
		if(in[k]!=1)
			return true;
	}

	return false;
}

int main(int argc, char** argv)
{	
	char filename[100];

	const char strfilenameeven[] = "leftovers/leftover.%d.even.txt";
	const char strfilenameodd[] = "leftovers/leftover.%d.%d.odd.txt";
	const char timingsnameeven[] = "timings/%d.even.time";
	const char timingsnameodd[] = "timings/%d.odd.time";
	mkdir("leftovers", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
	mkdir("timings", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

	in = fftw_alloc_complex(nchecks);
	out = fftw_alloc_complex(nchecks);
	p1 = fftw_plan_dft_1d(n, in, out, FFTW_FORWARD, FFTW_ESTIMATE);
	p2 = fftw_plan_dft_1d(nchecks, in, out, FFTW_FORWARD, FFTW_ESTIMATE);

	long totalfail = 0;
	long totalsuccess = 0;
	long totalcount = 0;

	sprintf(filename, strfilenameeven, n);
	FILE* f = fopen(filename, "w");
	if(f == NULL)
		fprintf(stderr, "File %s not opened.\n", filename), exit(0);

	clock_t start = clock();

	for(int s=0; s<=2; s++)
	{

		for(int i=0; i<nchecks; i++)
		{	in[i] = 0;
		}
		for(int i=0; i<n; i+=2)
		{	in[i] = 1;
		}

		if(s==1)
			in[2] = I;
		else if(s==2)
			in[2] = -1;

		do
		{
			if(!hall_pass_filter_fftw(&p1, n) && !hall_pass_filter_fftw(&p2, nchecks))
			{	totalfail++;
				fprint_in(f);
			}
			else
			{	totalsuccess++;
			}
			
			totalcount++;

		} while(next_arr_even());

	}

	clock_t end = clock();

	fclose(f);

	sprintf(filename, timingsnameeven, n);
	f = fopen(filename, "w");
	fprintf(f, "%.2f\n", (end-start)/(float)CLOCKS_PER_SEC);
	fclose(f);

	printf("Order %d even time: %.2f seconds, total: %ld, leftover: %ld (%.5Lf%%), filtered: %ld (%.5Lf%%)\n", n, (end-start)/(float)CLOCKS_PER_SEC, totalcount, totalfail, 100*totalfail/(long double)totalcount, totalsuccess, 100*(totalsuccess/(long double)totalcount));

	totalfail = 0;
	totalsuccess = 0;
	totalcount = 0;

	FILE* g[splits];
	for(int s=0; s<splits; s++)
	{	sprintf(filename, strfilenameodd, n, s);
		g[s] = fopen(filename, "w");
		if(g[s] == NULL)
			fprintf(stderr, "File %s not opened.\n", filename), exit(0);
	}

	start = clock();

	for(int i=0; i<nchecks; i++)
	{	in[i] = 0;
	}
	for(int i=1; i<n; i+=2)
	{	in[i] = 1;
	}

	do
	{
		if(!hall_pass_filter_fftw(&p1, n) && !hall_pass_filter_fftw(&p2, nchecks))
		{	totalfail++;
			fprint_in(g[totalcount%splits]);
		}
		else
		{	totalsuccess++;
		}
		
		totalcount++;

	} while(next_arr_odd());

	end = clock();

	for(int s=0; s<splits; s++)
		fclose(g[s]);

	sprintf(filename, timingsnameodd, n);
	f = fopen(filename, "w");
	fprintf(f, "%.2f\n", (end-start)/(float)CLOCKS_PER_SEC);
	fclose(f);

	printf("Order %d odd time: %.2f seconds, total: %ld, leftover: %ld (%.5Lf%%), filtered: %ld (%.5Lf%%)\n", n, (end-start)/(float)CLOCKS_PER_SEC, totalcount, totalfail, 100*totalfail/(long double)totalcount, totalsuccess, 100*(totalsuccess/(long double)totalcount));

	fftw_destroy_plan(p1);
	fftw_destroy_plan(p2);
	fftw_free(out);
	fftw_free(in);

	return 0;
}
