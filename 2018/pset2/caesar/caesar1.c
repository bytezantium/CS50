#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <cs50.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }

    // Converting k from string to integer
    int k = atoi(argv[1]);

    // Prompt user for plaintext input
    string ptext = get_string("plaintext:  ");

    // Print out ciphertext
    printf("ciphertext: ");

    // Character by character enciphering
    for (int i = 0, n = strlen(ptext); i < n; i++)
    {
        char c = ptext[i];

        // Check if character is alphabetical
        if (isalpha(c))
        {
            // Check if character isupper or islower
            if (isupper(c))
            {
                c = (((int) c + k) - 65) % 26;
                c += 65;
                c = (char) c;
            }
            else
            {
                c = (((int) c + k) - 97) % 26;
                c += 97;
                c = (char) c;
            }
        }

        printf("%c", c);
    }

    printf("\n");
    return 0;
}