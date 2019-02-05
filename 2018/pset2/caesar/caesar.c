// Encrypting single command-line non-negative integer arguments using Caesar's cipher


#include <cs50.h>
#include <stdio.h>
#include <string.h>
// Include stdlib.h for i.a. |atoi| to convert strings into integers
#include <stdlib.h>
// Include ctype.h for i.a. |isalpha| to iterate over ptext characters
#include <ctype.h>

// Declaring variables
string ptext;

int main(int argc, string argv[])
{
    // Print error and return 1 from main if user does not input single command line argument
    if (argc < 2 || argc > 2)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }

    // Initializing integer key (k) by converting from the string the user inputted
    int k = atoi(argv[1]);

    // Prompt user for a string of plaintext
    {
        ptext = get_string("plaintext:  ");
    }

    printf("ciphertext: ");

    for (int i = 0, n = strlen(ptext); i < n; i++)
    {
        char pc = ptext[i];
        if (isalpha(pc))
        {
            // Check if character isupper and shift
            if (isupper(pc))
            {
                pc = (((int) pc + k) - 65) % 26;
                pc += 65;
                pc = (char) pc;
            }

            // Isupper false --> Shift lower case character
            else
            {
                pc = (((int) pc + k) - 97) % 26;
                pc += 97;
                pc = (char) pc;
            }

            printf("%c", pc);
        }

        else
        {
            printf("%c", pc);
        }

    }

    printf("\n");
    return 0;
}