#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <cs50.h>

// Global variable
string key;

// Functions
bool is_key_alpha(string x);

int main(int argc, string argv[])
{
    if (argc != 2 || !is_key_alpha(argv[1]))
    {
        printf("Usage: ./caesar alphabetical k\n");
        return 1;
    }

    // Prompt user for plaintext input
    string ptext = get_string("plaintext:  ");

    // Print out ciphertext
    printf("ciphertext: ");

    // Character by character enciphering
    for (int i = 0, j = 0, n = strlen(ptext); i < n; i++)
    {
        char c = ptext[i];

        // Check if character is alphabetical and encipher with rotating kj

        if (!isalpha(c))
        {
            printf("%c", c);
        }

        else
        {
            // Initializing kj and convert from string to integer
            key = argv[1];
            int key_len = strlen(key);
            char kj = key[j % key_len];
            kj = (int) kj;

            // Assigning k it's alphabetical 0 - 25 number
            if (kj < 91)
            {
                kj -= 65;
            }
            else
            {
                kj -= 97;
            }

            // Check if character isupper or islower
            if (isupper(c))
            {
                c = (((int) c + kj) - 65) % 26;
                c += 65;
                c = (char) c;
            }
            else
            {
                c = (((int) c + kj) - 97) % 26;
                c += 97;
                c = (char) c;
            }

            printf("%c", c);
            j++;
        }

    }

    printf("\n");
    return 0;
}

// Functions
bool is_key_alpha(string x)
{
    for (int l = 0; l < strlen(x); l++)
    {
        if (!isalpha(x[l]))
        {
            return false;
        }
    }

    return true;
}