#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <sys/types.h>
#include <sys/stat.h>
#include "decomps.h"

int main(int argc, char** argv) 
{
	char filename[100];

	if(argc==1)
		std::cerr << "Need order of paired PAF matching files to join\n", exit(0);

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

	mkdir("matchedpairs", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

	const char seqnsfilename[] = "matchings/%d.%d.%d.%s.seqns.txt";
	const char pafsfilename[] = "matchings/%d.%d.%d.%s.pafs.sorted.txt";
	const char matchedfilename[] = "matchedpairs/%d.%d.%d";

	printf("ORDER %d: Join compression sequence pairs\n", n);

	std::ifstream file;
	std::string str;
	std::vector<std::string> Aseqns;
	sprintf(filename, seqnsfilename, n, 0, l, "A");
	file.open(filename);
	while(std::getline(file, str))
		Aseqns.push_back(str);
	file.close();

	for(int c = 0; c < decomps_len[n]; c++)
	{
		if(casetosolve != -1 && casetosolve != c)
			continue;

		clock_t start = clock();

		std::vector<std::string> Bseqns, Cseqns, Dseqns, ABseqns, CDseqns;
		std::ofstream outfile;

		sprintf(filename, seqnsfilename, n, c, l, "B");
		file.open(filename);
		while(std::getline(file, str))
			Bseqns.push_back(str);
		file.close();

		sprintf(filename, seqnsfilename, n, c, l, "C");
		file.open(filename);
		while(std::getline(file, str))
			Cseqns.push_back(str);
		file.close();

		sprintf(filename, seqnsfilename, n, c, l, "D");
		file.open(filename);
		while(std::getline(file, str))
			Dseqns.push_back(str);
		file.close();

		std::string ABstr, CDstr;
		std::ifstream ABfile, CDfile;

		sprintf(filename, pafsfilename, n, c, l, "AB");
		ABfile.open(filename);
		sprintf(filename, pafsfilename, n, c, l, "CD");
		CDfile.open(filename);

		int colonind;
		std::size_t sz;
		int ABind1, ABind2, CDind1, CDind2;
		int seqncount = 0;
		bool ABend = false, CDend = false;

		if(std::getline(ABfile, str))
		{	colonind = str.find_first_of(":");
			ABind1 = std::stoi(str.substr(colonind+2), &sz);
			ABind2 = std::stoi(str.substr(colonind+2+sz));
			ABstr = str.substr(0, colonind);
		}
		else
			ABend = CDend = true;

		if(std::getline(CDfile, str))
		{	colonind = str.find_first_of(":");
			CDind1 = std::stoi(str.substr(colonind+2), &sz);
			CDind2 = std::stoi(str.substr(colonind+2+sz));
			CDstr = str.substr(0, colonind);
		}
		else
			ABend = CDend = true;

		sprintf(filename, matchedfilename, n, c, l);
		outfile.open(filename);

		while(!(ABend && CDend))
		{	if(ABstr == CDstr)
			{	//std::cout << ABstr << "= " << CDstr << '\n';
				std::string eqstr = ABstr;
				while(ABstr == eqstr)
				{	
					ABseqns.push_back(Aseqns[ABind1]+Bseqns[ABind2]);
					if(std::getline(ABfile, str))
					{	colonind = str.find_first_of(":");
						ABind1 = std::stoi(str.substr(colonind+2), &sz);
						ABind2 = std::stoi(str.substr(colonind+2+sz));
						ABstr = str.substr(0, colonind);
					}
					else
					{	ABend = true;
						break;
					}
				}
				while(CDstr == eqstr)
				{	
					CDseqns.push_back(Cseqns[CDind1]+Dseqns[CDind2]);
					if(std::getline(CDfile, str))
					{	colonind = str.find_first_of(":");
						CDind1 = std::stoi(str.substr(colonind+2), &sz);
						CDind2 = std::stoi(str.substr(colonind+2+sz));
						CDstr = str.substr(0, colonind);
					}
					else
					{	CDend = true;
						break;
					}
				}

				for(int i=0; i<CDseqns.size(); i++)
					for(int j=0; j<ABseqns.size(); j++)
					{	outfile << ABseqns[j] << CDseqns[i] << '\n';
						seqncount++;
					}

				ABseqns.clear();
				CDseqns.clear();
			}
			else if(ABstr < CDstr)
			{	//std::cout << ABstr << "< " << CDstr << '\n';
				if(std::getline(ABfile, str))
				{	colonind = str.find_first_of(":");
					ABind1 = std::stoi(str.substr(colonind+2), &sz);
					ABind2 = std::stoi(str.substr(colonind+2+sz));
					ABstr = str.substr(0, colonind);
				}
				else
				{	ABend = true;
					break;
				}
			}
			else
			{	//std::cout << ABstr << "> " << CDstr << '\n';
				if(std::getline(CDfile, str))
				{	colonind = str.find_first_of(":");
					CDind1 = std::stoi(str.substr(colonind+2), &sz);
					CDind2 = std::stoi(str.substr(colonind+2+sz));
					CDstr = str.substr(0, colonind);
				}
				else
				{	CDend = true;
					break;
				}
			}
		}

		ABfile.close();
		CDfile.close();
		outfile.close();

		sprintf(filename, "timings/%d.%d.%d.jointime", n, c, l);
		FILE* f = fopen(filename, "w");
		fprintf(f, "%.2f\n", (clock() - start)/(float)CLOCKS_PER_SEC);
		fclose(f);

		printf("  Case %d: %d matched sequence pairs of length %d generated in %.2f seconds\n", c, seqncount, l, (clock() - start)/(float)CLOCKS_PER_SEC);

	}

}
