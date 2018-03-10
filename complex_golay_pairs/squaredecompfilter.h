#if N == 2
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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
const bool decomps[9][9] = {
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

bool square_decomp_filter(const fftw_complex* evens_dft, const std::array<fftw_complex, NC>& odds_dft)
{
	// Check sums-of-squares decomposition of A
	{
		const int x = abs(round(evens_dft[0][0]+odds_dft[0][0]));
		const int y = abs(round(evens_dft[0][1]+odds_dft[0][1]));

		if(decomps[x][y]==false)
			return true;

	}
	// Check sums-of-squares decomposition of (-1) \star A
	{
		const int x = abs(round(evens_dft[NC/2][0]+odds_dft[NC/2][0]));
		const int y = abs(round(evens_dft[NC/2][1]+odds_dft[NC/2][1]));

		if(decomps[x][y]==false)
			return true;

	}
	// Check sums-of-squares decomposition of i \star A
	{
		const int x = abs(round(evens_dft[NC/4][0]+odds_dft[NC/4][0]));
		const int y = abs(round(evens_dft[NC/4][1]+odds_dft[NC/4][1]));

		if(decomps[x][y]==false)
			return true;

	}
	// Check sums-of-squares decomposition of (-i) \star A
	{
		const int x = abs(round(evens_dft[3*NC/4][0]+odds_dft[3*NC/4][0]));
		const int y = abs(round(evens_dft[3*NC/4][1]+odds_dft[3*NC/4][1]));

		if(decomps[x][y]==false)
			return true;

	}

	return false;
}
