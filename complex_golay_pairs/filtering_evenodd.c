#include <math.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <complex.h>
#include <fftw3.h>
#include <sys/types.h>
#include <sys/stat.h>
#ifdef DEBUG
#include "assert.h"
#endif

#define NC 128
#ifndef NUMSPLITS
#define NUMSPLITS 1
#endif
#define INTERPOLATE

fftwf_complex* in;
fftwf_complex* out;
fftwf_plan p;

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

#ifdef INTERPOLATE
float hall(const float theta)
{	
	fftwf_complex r = 0;
	for(int k=0; k<n; k++)
	{	r += in[k]*cexpf(-I*theta*k);
	}
	const float re = crealf(r);
	const float im = cimagf(r);
	const float psd = re*re+im*im;
	return psd;
}

#ifdef DEBUG
long iterations = 0;
long total = 0;
#endif

bool interpolation_filter(float x1, float x2, float x3, float f1, float f2, float f3)
{
	float x4 = 0.5*(f1*(x2*x2-x3*x3)+f2*(x3*x3-x1*x1)+f3*(x1*x1-x2*x2))/(f1*(x2-x3)+f2*(x3-x1)+f3*(x1-x2));
	float f4 = hall(x4);

#ifdef DEBUG
	iterations++;
#endif
	if(f4 - 2*n > 0.001)
		return true;

	for(int i=0; i<2; i++)
	{
		if(x4 > x2 && f4 <= f2)
		{	
			x3 = x4;
			f3 = f4;
		}
		else if(x4 > x2 && f4 > f2)
		{	
			x1 = x2;
			f1 = f2;
			x2 = x4;
			f2 = f4;
		}
		else if(x4 < x2 && f4 < f2)
		{	
			x1 = x4;
			f1 = f4;
		}
		else if(x4 < x2 && f4 >= f2)
		{	
			x3 = x2;
			f3 = f2;
			x2 = x4;
			f2 = f4;
		}

#ifdef DEBUG
		iterations++;
#endif
		x4 = 0.5*(f1*(x2*x2-x3*x3)+f2*(x3*x3-x1*x1)+f3*(x1*x1-x2*x2))/(f1*(x2-x3)+f2*(x3-x1)+f3*(x1-x2));
		f4 = hall(x4);

		if(f4 - 2*n > 0.001)
			return true;

		if(fabsf(x4-x2) < 0.01)
			break;
	}

	return false;
}
#endif

bool hall_pass_filter_fftw(const fftwf_plan* p, int const len)
{	
	float psds[len];
	float max_psd = 0;

	fftwf_execute(*p);

	for(int k=0; k<len; k++)
	{	const float rout = crealf(out[k]);
		const float iout = cimagf(out[k]);
		const float psd = rout*rout+iout*iout;

		if(psd - 2*n > 0.001)
			return true;

		if(psd > max_psd)
			max_psd = psd;

		psds[k] = psd;
	}

	#ifdef INTERPOLATE
	for(int k=0; k<len; k++)
	{	const float f1 = psds[(k+len-1)%len];
		const float f2 = psds[k];
		const float f3 = psds[(k+1)%len];

		if(f2 == max_psd || (f1 <= f2 && f2 <= f3 && f2 >= n))
			if(interpolation_filter(2*M_PI*(k-1)/(float)len, 2*M_PI*k/(float)len, 2*M_PI*(k+1)/(float)len, f1, f2, f3))
				return true;
	}
	#endif

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

	in = fftwf_alloc_complex(nchecks);
	out = fftwf_alloc_complex(nchecks);
	p = fftwf_plan_dft_1d(nchecks, in, out, FFTW_FORWARD, FFTW_ESTIMATE);

#ifndef SKIPEVEN
	{
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
			if(!hall_pass_filter_fftw(&p, nchecks))
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
	}
#endif

#ifndef SKIPODD
	long totalfail = 0;
	long totalsuccess = 0;
	long totalcount = 0;

	FILE* g[splits];
	for(int s=0; s<splits; s++)
	{	sprintf(filename, strfilenameodd, n, s);
		g[s] = fopen(filename, "w");
		if(g[s] == NULL)
			fprintf(stderr, "File %s not opened.\n", filename), exit(0);
	}

	clock_t start = clock();

	for(int i=0; i<nchecks; i++)
	{	in[i] = 0;
	}
	for(int i=1; i<n; i+=2)
	{	in[i] = 1;
	}

	do
	{
		if(!hall_pass_filter_fftw(&p, nchecks))
		{	totalfail++;
			fprint_in(g[totalcount%splits]);
		}
		else
		{	totalsuccess++;
		}
		
		totalcount++;

	} while(next_arr_odd());

	clock_t end = clock();

	for(int s=0; s<splits; s++)
		fclose(g[s]);

	sprintf(filename, timingsnameodd, n);
	FILE* f = fopen(filename, "w");
	fprintf(f, "%.2f\n", (end-start)/(float)CLOCKS_PER_SEC);
	fclose(f);

	printf("Order %d odd time: %.2f seconds, total: %ld, leftover: %ld (%.5Lf%%), filtered: %ld (%.5Lf%%)\n", n, (end-start)/(float)CLOCKS_PER_SEC, totalcount, totalfail, 100*totalfail/(long double)totalcount, totalsuccess, 100*(totalsuccess/(long double)totalcount));
#endif

	#if defined(INTERPOLATE) && defined(DEBUG)
	printf("%ld/%ld = %.2f\n", iterations, total, iterations/(double)total);
	#endif

	fftwf_destroy_plan(p);
	fftwf_free(out);
	fftwf_free(in);

	return 0;
}
