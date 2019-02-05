// CS50x Pset1/More/Credit

#include <cs50.h>
#include <stdio.h>

// Prototype
int sum(long long number, long long x, int y);

// Global variables
long long cc_number;
long long divisor = 10;
int i = 0; // for custom function recursive cases

int main(void)
{
    // Prompt for user input
    do
    {
        cc_number = get_long_long("Creditcard number: ");
    }
    while (cc_number <= 0);

    // Validate checksum
    if (sum(cc_number, divisor, i) % 10 != 0)
    {
        printf("INVALID\n");
    }
    // Validate company's identifier and number's length
    if ((cc_number >= 4000000000000 && cc_number < 5000000000000) || (cc_number >= 4000000000000000 && cc_number < 5000000000000000))
    {
        printf("VISA\n");
    }
    if ((cc_number >= 340000000000000 && cc_number < 350000000000000) || (cc_number >= 370000000000000 && cc_number < 380000000000000))
    {
        printf("AMEX\n");
    }
    if (cc_number >= 5100000000000000 && cc_number < 5600000000000000)
    {
        printf("MASTERCARD\n");
    }
    else
    {
        printf("INVALID\n");
    }

    // success
    return 0;
}

// Custom function
int sum(long long number, long long x, int y)
{
    int digit = number % 10;

    if (number > 5) // Recursive cases
    {
        if (y == 0) // every other
        {
            return digit + sum(number / x, x, y = 1);
        }
        else // every second-to-last
        {
            digit *= 2;
            return (digit % 10) + ((digit / 10) % 10) + sum(number / x, x, y = 0);
        }
    }

    else if (y == 1) // Base Case 1
    {
        digit *= 2;
        return (digit % 10) + ((digit / 10) % 10);
    }

    return digit; // Base Case 2
}


