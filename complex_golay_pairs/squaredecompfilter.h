#include "decomps.h"

#if N == 2
const bool bool_decomps[9][9] = {
{ true, false, true, false, false, false, false, false },
{ false, true, false, false, false, false, false, false },
{ true, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 3
const bool bool_decomps[9][9] = {
{ false, true, false, false, false, false, false, false },
{ true, false, true, false, false, false, false, false },
{ false, true, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 4
const bool bool_decomps[9][9] = {
{ true, false, true, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ true, false, true, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 5
const bool bool_decomps[9][9] = {
{ false, true, false, true, false, false, false, false },
{ true, false, true, false, false, false, false, false },
{ false, true, false, false, false, false, false, false },
{ true, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 6
const bool bool_decomps[9][9] = {
{ false, false, true, false, false, false, false, false },
{ false, true, false, true, false, false, false, false },
{ true, false, true, false, false, false, false, false },
{ false, true, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 7
const bool bool_decomps[9][9] = {
{ false, true, false, true, false, false, false, false },
{ true, false, true, false, false, false, false, false },
{ false, true, false, true, false, false, false, false },
{ true, false, true, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 8
const bool bool_decomps[9][9] = {
{ true, false, false, false, true, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, true, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ true, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 9
const bool bool_decomps[9][9] = {
{ false, true, false, true, false, false, false, false },
{ true, false, true, false, true, false, false, false },
{ false, true, false, true, false, false, false, false },
{ true, false, true, false, false, false, false, false },
{ false, true, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 10
const bool bool_decomps[9][9] = {
{ true, false, true, false, true, false, false, false },
{ false, true, false, true, false, false, false, false },
{ true, false, false, false, true, false, false, false },
{ false, true, false, true, false, false, false, false },
{ true, false, true, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 11
const bool bool_decomps[9][9] = {
{ false, false, false, true, false, false, false, false },
{ false, false, true, false, true, false, false, false },
{ false, true, false, true, false, false, false, false },
{ true, false, true, false, false, false, false, false },
{ false, true, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 12
const bool bool_decomps[9][9] = {
{ false, false, true, false, true, false, false, false },
{ false, false, false, false, false, false, false, false },
{ true, false, true, false, true, false, false, false },
{ false, false, false, false, false, false, false, false },
{ true, false, true, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 13
const bool bool_decomps[9][9] = {
{ false, true, false, true, false, true, false, false },
{ true, false, false, false, true, false, false, false },
{ false, false, false, true, false, false, false, false },
{ true, false, true, false, true, false, false, false },
{ false, true, false, true, false, false, false, false },
{ true, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 14
const bool bool_decomps[9][9] = {
{ false, false, false, false, false, false, false, false },
{ false, true, false, true, false, true, false, false },
{ false, false, true, false, true, false, false, false },
{ false, true, false, true, false, false, false, false },
{ false, false, true, false, false, false, false, false },
{ false, true, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 15
const bool bool_decomps[9][9] = {
{ false, true, false, false, false, true, false, false },
{ true, false, true, false, true, false, false, false },
{ false, true, false, true, false, true, false, false },
{ false, false, true, false, true, false, false, false },
{ false, true, false, true, false, false, false, false },
{ true, false, true, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 16
const bool bool_decomps[9][9] = {
{ true, false, false, false, true, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ true, false, false, false, true, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 17
const bool bool_decomps[9][9] = {
{ false, false, false, true, false, true, false, false },
{ false, false, true, false, true, false, false, false },
{ false, true, false, false, false, true, false, false },
{ true, false, false, false, true, false, false, false },
{ false, true, false, true, false, false, false, false },
{ true, false, true, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 18
const bool bool_decomps[9][9] = {
{ true, false, true, false, true, false, true, false },
{ false, true, false, true, false, true, false, false },
{ true, false, false, false, true, false, false, false },
{ false, true, false, true, false, true, false, false },
{ true, false, true, false, true, false, false, false },
{ false, true, false, true, false, false, false, false },
{ true, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 19
const bool bool_decomps[9][9] = {
{ false, true, false, true, false, true, false, false },
{ true, false, false, false, false, false, true, false },
{ false, false, false, true, false, true, false, false },
{ true, false, true, false, true, false, false, false },
{ false, false, false, true, false, false, false, false },
{ true, false, true, false, false, false, false, false },
{ false, true, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 20
const bool bool_decomps[9][9] = {
{ true, false, true, false, false, false, true, false },
{ false, false, false, false, false, false, false, false },
{ true, false, true, false, true, false, true, false },
{ false, false, false, false, false, false, false, false },
{ false, false, true, false, true, false, false, false },
{ false, false, false, false, false, false, false, false },
{ true, false, true, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 21
const bool bool_decomps[9][9] = {
{ false, true, false, false, false, true, false, false },
{ true, false, true, false, true, false, true, false },
{ false, true, false, true, false, true, false, false },
{ false, false, true, false, true, false, false, false },
{ false, true, false, true, false, true, false, false },
{ true, false, true, false, true, false, false, false },
{ false, true, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 22
const bool bool_decomps[9][9] = {
{ false, false, true, false, false, false, true, false },
{ false, false, false, true, false, true, false, false },
{ true, false, true, false, false, false, true, false },
{ false, true, false, true, false, true, false, false },
{ false, false, false, false, false, false, false, false },
{ false, true, false, true, false, false, false, false },
{ true, false, true, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 23
const bool bool_decomps[9][9] = {
{ false, true, false, true, false, false, false, false },
{ true, false, true, false, true, false, true, false },
{ false, true, false, false, false, true, false, false },
{ true, false, false, false, false, false, true, false },
{ false, true, false, false, false, true, false, false },
{ false, false, true, false, true, false, false, false },
{ false, true, false, true, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 24
const bool bool_decomps[9][9] = {
{ false, false, false, false, true, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, true, false, false, false, true, false },
{ false, false, false, false, false, false, false, false },
{ true, false, false, false, true, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, true, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 25
const bool bool_decomps[9][9] = {
{ false, true, false, true, false, true, false, true },
{ true, false, true, false, false, false, true, false },
{ false, true, false, true, false, false, false, false },
{ true, false, true, false, true, false, true, false },
{ false, false, false, true, false, true, false, false },
{ true, false, false, false, true, false, false, false },
{ false, true, false, true, false, false, false, false },
{ true, false, false, false, false, false, false, false },
};
#elif N == 26
const bool bool_decomps[9][9] = {
{ true, false, false, false, true, false, true, false },
{ false, true, false, false, false, true, false, true },
{ false, false, false, false, true, false, false, false },
{ false, false, false, true, false, true, false, false },
{ true, false, true, false, true, false, true, false },
{ false, true, false, true, false, true, false, false },
{ true, false, false, false, true, false, false, false },
{ false, true, false, false, false, false, false, false },
};
#elif N == 27
const bool bool_decomps[9][9] = {
{ false, true, false, true, false, true, false, true },
{ true, false, true, false, true, false, true, false },
{ false, true, false, true, false, true, false, true },
{ true, false, true, false, true, false, true, false },
{ false, true, false, true, false, true, false, false },
{ true, false, true, false, true, false, false, false },
{ false, true, false, true, false, false, false, false },
{ true, false, true, false, false, false, false, false },
};
#elif N == 28
const bool bool_decomps[9][9] = {
{ false, false, true, false, true, false, true, false },
{ false, false, false, false, false, false, false, false },
{ true, false, false, false, true, false, true, false },
{ false, false, false, false, false, false, false, false },
{ true, false, true, false, false, false, true, false },
{ false, false, false, false, false, false, false, false },
{ true, false, true, false, true, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 29
const bool bool_decomps[9][9] = {
{ false, false, false, true, false, false, false, true },
{ false, false, true, false, true, false, false, false },
{ false, true, false, true, false, true, false, true },
{ true, false, true, false, false, false, true, false },
{ false, true, false, false, false, true, false, false },
{ false, false, true, false, true, false, false, false },
{ false, false, false, true, false, false, false, false },
{ true, false, true, false, false, false, false, false },
};
#elif N == 30
const bool bool_decomps[9][9] = {
{ false, false, false, false, false, false, false, false },
{ false, true, false, true, false, true, false, true },
{ false, false, true, false, true, false, true, false },
{ false, true, false, false, false, true, false, true },
{ false, false, true, false, false, false, true, false },
{ false, true, false, true, false, true, false, false },
{ false, false, true, false, true, false, false, false },
{ false, true, false, true, false, false, false, false },
};
#elif N == 31
const bool bool_decomps[9][9] = {
{ false, true, false, true, false, true, false, true },
{ true, false, false, false, true, false, true, false },
{ false, false, false, true, false, false, false, true },
{ true, false, true, false, true, false, true, false },
{ false, true, false, true, false, false, false, false },
{ true, false, false, false, false, false, true, false },
{ false, true, false, true, false, true, false, false },
{ true, false, true, false, false, false, false, false },
};
#elif N == 32
const bool bool_decomps[9][9] = {
{ true, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, true, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 33
const bool bool_decomps[9][9] = {
{ false, true, false, false, false, true, false, true },
{ true, false, true, false, true, false, true, false },
{ false, true, false, true, false, true, false, true },
{ false, false, true, false, true, false, false, false },
{ false, true, false, true, false, true, false, true },
{ true, false, true, false, true, false, true, false },
{ false, true, false, false, false, true, false, false },
{ true, false, true, false, true, false, false, false },
};
#elif N == 34
const bool bool_decomps[9][9] = {
{ true, false, true, false, true, false, true, false },
{ false, false, false, true, false, false, false, true },
{ true, false, false, false, false, false, false, false },
{ false, true, false, true, false, true, false, true },
{ true, false, false, false, true, false, true, false },
{ false, false, false, true, false, true, false, false },
{ true, false, false, false, true, false, false, false },
{ false, true, false, true, false, false, false, false },
};
#elif N == 35
const bool bool_decomps[9][9] = {
{ false, false, false, true, false, true, false, false },
{ false, false, true, false, true, false, false, false },
{ false, true, false, false, false, true, false, true },
{ true, false, false, false, true, false, true, false },
{ false, true, false, true, false, true, false, true },
{ true, false, true, false, true, false, true, false },
{ false, false, false, true, false, true, false, false },
{ false, false, true, false, true, false, false, false },
};
#elif N == 36
const bool bool_decomps[9][9] = {
{ true, false, true, false, false, false, true, false },
{ false, false, false, false, false, false, false, false },
{ true, false, true, false, true, false, true, false },
{ false, false, false, false, false, false, false, false },
{ false, false, true, false, true, false, true, false },
{ false, false, false, false, false, false, false, false },
{ true, false, true, false, true, false, true, false },
{ false, false, false, false, false, false, false, false },
};
#elif N == 37
const bool bool_decomps[9][9] = {
{ false, true, false, true, false, true, false, true },
{ true, false, false, false, false, false, true, false },
{ false, false, false, true, false, true, false, false },
{ true, false, true, false, true, false, true, false },
{ false, false, false, true, false, false, false, true },
{ true, false, true, false, false, false, true, false },
{ false, true, false, true, false, true, false, false },
{ true, false, false, false, true, false, false, false },
};
#elif N == 38
const bool bool_decomps[9][9] = {
{ false, false, true, false, false, false, true, false },
{ false, true, false, false, false, true, false, true },
{ true, false, true, false, false, false, true, false },
{ false, false, false, true, false, false, false, true },
{ false, false, false, false, false, false, false, false },
{ false, true, false, false, false, true, false, true },
{ true, false, true, false, false, false, true, false },
{ false, true, false, true, false, true, false, false },
};
#elif N == 39
const bool bool_decomps[9][9] = {
{ false, false, false, false, false, true, false, true },
{ false, false, true, false, true, false, true, false },
{ false, true, false, true, false, true, false, true },
{ false, false, true, false, true, false, false, false },
{ false, true, false, true, false, true, false, true },
{ true, false, true, false, true, false, true, false },
{ false, true, false, false, false, true, false, false },
{ true, false, true, false, true, false, false, false },
};
#elif N == 40
const bool bool_decomps[9][9] = {
{ true, false, false, false, true, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, true, false, false, false, true, false },
{ false, false, false, false, false, false, false, false },
{ true, false, false, false, false, false, false, false },
{ false, false, false, false, false, false, false, false },
{ false, false, true, false, false, false, true, false },
{ false, false, false, false, false, false, false, false },
};
#endif

bool square_decomp_filter(const std::array<fftwf_complex, NC>& evens_dft, const std::array<fftwf_complex, NC>& odds_dft)
{
	// Check sums-of-squares decomposition of (-1) \star A
	{
		const int x = abs(roundf(evens_dft[NC/2][0]+odds_dft[NC/2][0]));
		const int y = abs(roundf(evens_dft[NC/2][1]+odds_dft[NC/2][1]));

		if(bool_decomps[x][y]==false)
			return true;

	}
	// Check sums-of-squares decomposition of (-i) \star A
	{
		const int x = abs(roundf(evens_dft[3*NC/4][0]+odds_dft[3*NC/4][0]));
		const int y = abs(roundf(evens_dft[3*NC/4][1]+odds_dft[3*NC/4][1]));

		if(bool_decomps[x][y]==false)
			return true;

	}

	return false;
}
