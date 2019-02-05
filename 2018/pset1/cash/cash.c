#include <stdio.h>
#include <cs50.h>

// For rounding
#include <math.h>
double round(double n);

// Initializing float change Dollars and int change Cents
float Dchange;
int Cchange;

int main(void)
{
    // Prompting user for amount of change owed and converting from dollars into cents
    do
    {
        Dchange = get_float("Change owed: ");
        Cchange = round(Dchange * 100);
    }
    while (Cchange <= 0);

    // Declare quarter, dime, nickel and penny counters
    int qcounter, dcounter, ncounter, pcounter;
    qcounter = Cchange / 25;
    dcounter = (Cchange % 25) / 10;
    ncounter = ((Cchange % 25) % 10) / 5;
    pcounter = (((Cchange % 25) % 10) % 5) / 1;
    {
        printf("%i\n", qcounter + dcounter + ncounter + pcounter);
    }
}