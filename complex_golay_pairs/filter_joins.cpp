#include <math.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <fftw3.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <array>
#include <vector>
#include <assert.h>

#define INTERPOLATE
#define MAX_SIZE N
#define NC 1024

const int nchecks = NC;
const int n = N;

std::vector<std::array<fftwf_complex, MAX_SIZE>> odds;
std::vector<std::array<fftwf_complex, MAX_SIZE>> evens;

fftwf_complex* in;
fftwf_complex* out;
fftwf_plan p;

void fprint_join(FILE* f)
{	for(int k=0; k<n; k++)
	{	if(in[k][0]==1)
			fprintf(f, "+");
		else if(in[k][0]==-1)
			fprintf(f, "-");
		else if(in[k][1]==1)
			fprintf(f, "i");
		else if(in[k][1]==-1)
			fprintf(f, "j");
		else
			fprintf(f, "*");
	}
	fprintf(f, "\n");
}

#ifdef INTERPOLATE
float hall(float theta)
{	
	__complex__ float r = 0;
	for(int k=0; k<n; k++)
	{	r += (in[k][0]+I*in[k][1])*cexpf(-I*theta*k);
	}
	const float re = crealf(r);
	const float im = cimagf(r);
	const float psd = re*re+im*im;
	return psd;
}

bool interpolation_filter(float x1, float x2, float x3, float f1, float f2, float f3)
{
	float x4 = 0.5*(f1*(x2*x2-x3*x3)+f2*(x3*x3-x1*x1)+f3*(x1*x1-x2*x2))/(f1*(x2-x3)+f2*(x3-x1)+f3*(x1-x2));
	float f4 = hall(x4);

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

bool hall_pass_filter()
{	
	float psds[NC];
	float max_psd = 0;
	
	for(int l=0; l<NC; l++)
	{		
		const float psd = out[l][0]*out[l][0]+out[l][1]*out[l][1];
		
		if(psd - 2*n > 0.001)
			return true;

		if(max_psd < psd)
			max_psd = psd;	

		psds[l] = psd;
	}
	
	#ifdef INTERPOLATE
	for(int k=0; k<NC; k++)
	{	const float f1 = psds[(k+NC-1)%NC];
		const float f2 = psds[k];
		const float f3 = psds[(k+1)%NC];

		if(f2 == max_psd || (f1 <= f2 && f2 <= f3 && f2 >= n))
			if(interpolation_filter(2*M_PI*(k-1)/(float)NC, 2*M_PI*k/(float)NC, 2*M_PI*(k+1)/(float)NC, f1, f2, f3))
				return true;
	}
	#endif

	return false;
}

int main(int argc, char** argv)
{	
	char filename[100];
	clock_t start = clock();

	const char strfilenameeven[] = "leftovers/leftover.%d.even.txt";
	const char strfilenameodd[] = "leftovers/leftover.%d.%d.odd.txt";
	const char strfilenamejoins[] = "joinsums/joinsums.%d.%d.txt";
	const char strfilenameout[] = "joins/join.%d.%d.txt";
	const char timingsname[] = "timings/%d.%d.genjoin.time";
	mkdir("joins", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
	mkdir("timings", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

	in = fftwf_alloc_complex(nchecks);
	out = fftwf_alloc_complex(nchecks);
	p = fftwf_plan_dft_1d(nchecks, in, out, FFTW_BACKWARD, FFTW_ESTIMATE);

	odds.clear();
	evens.clear();

	for(int i=0; i<nchecks; i++)
	{	in[i][0] = 0, in[i][1] = 0;
	}

	sprintf(filename, strfilenameeven, n);
	FILE* f = fopen(filename, "r");
	if(f == NULL)
		fprintf(stderr, "File %s not opened.\n", filename), exit(0);

	std::array<fftwf_complex, MAX_SIZE> A = {};
	int c = 0;
	int i = 0;
	while(c != EOF)
	{	
		c = fgetc(f);
		if(c=='+')
		{	A[i][0] = 1, A[i][1] = 0;
		}
		else if(c=='-')
		{	A[i][0] = -1, A[i][1] = 0;
		}
		else if(c=='i')
		{	A[i][0] = 0, A[i][1] = 1;
		}
		else if(c=='j')
		{	A[i][0] = 0, A[i][1] = -1;
		}
		else if(c=='\n')
		{	i = -1;
			evens.push_back(A);
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

	std::array<fftwf_complex, MAX_SIZE> B = {};
	c = 0;
	i = 0;
	while(c != EOF)
	{	
		c = fgetc(g);
		if(c=='+')
		{	B[i][0] = 1, B[i][1] = 0;
		}
		else if(c=='-')
		{	B[i][0] = -1, B[i][1] = 0;
		}
		else if(c=='i')
		{	B[i][0] = 0, B[i][1] = 1;
		}
		else if(c=='j')
		{	B[i][0] = 0, B[i][1] = -1;
		}
		else if(c=='\n')
		{	i = -1;
			odds.push_back(B);
		}
		i++;
	}
	
	fclose(g);

	sprintf(filename, strfilenamejoins, n, splitsnum);
	FILE* h = fopen(filename, "r");
	if(h == NULL)
		fprintf(stderr, "File %s not opened.\n", filename), exit(0);

	int total = 0, notfiltered = 0;
	int E_index, O_index;

	sprintf(filename, strfilenameout, n, splitsnum);
	FILE* outf = fopen(filename, "w");
	if(outf == NULL)
		fprintf(stderr, "File %s not opened.\n", filename), exit(0);

	do
	{
		total++;
		int ret = fscanf(h, "%d %d\n", &E_index, &O_index);
		assert(ret == 2);
		
		for(int k=0; k<N; k++)
		{	in[k][0] = evens[E_index][k][0] + odds[O_index][k][0];
			in[k][1] = evens[E_index][k][1] + odds[O_index][k][1];
		}

		fftwf_execute(p);

		if(!hall_pass_filter())
		{	fprint_join(outf);
			notfiltered++;
		}
	} while(!feof(h));

	fclose(h);
	fclose(outf);

	sprintf(filename, timingsname, n, splitsnum);
	h = fopen(filename, "w");
	fprintf(h, "%.2f\n", (clock() - start)/(float)CLOCKS_PER_SEC);
	fclose(h);

	printf("  Generated %d/%d sequences (filtered %.5f%%) from join data in %.2f seconds\n", notfiltered, total, 100*(1-notfiltered/(double)total), (clock() - start)/(float)CLOCKS_PER_SEC);

	fftwf_destroy_plan(p);
	fftwf_free(out);
	fftwf_free(in);

	return 0;
}
