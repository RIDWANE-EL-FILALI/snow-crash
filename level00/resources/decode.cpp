#include <iostream>

int main()
{
	std::string tab = "cdiiddwpgswtgt";

	int i = 1;
	while (i < 26)
	{
		for (int j =0; j < tab.size();j++)
		{
			tab[j] = 'a' + (tab[j] - 'a' - i  + 26) % 26;
		}
		i++;
		std::cout << tab << std::endl;
		tab = "cdiiddwpgswtgt";
	}
	return (0);
}
