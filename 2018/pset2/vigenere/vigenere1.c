#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

// Declaring functions
bool is_alpha(string x);

// one string command line argument
int main(int argc, string argv[])
{
    // Check for valid command line arguments
    if (argc != 2 || !is_alpha(argv[1]))
    {
        fprintf(stderr, "Usage: ./vigenere k (alphabetical)\n");
        return 1;
    }

    // Prompt user for plaintext input
    string plaintext = get_string("plaintext:  ");

    // Print ciphertext
    printf("ciphertext: ");

    // Extract plaintext alphabetical characters and encipher one by one using vigenere key method (rotation)
    for (int i = 0, j = 0, n = strlen(plaintext); i < n; i++)
    {
        char pi = plaintext[i];

        // check if pi is alphabetic
        if (!isalpha(pi))
        {
            printf("%c", pi);
        }

        else
        {
            // Parse string from command line arguments array and get length of string
            string key = argv[1];
            int key_len = strlen(key);

            // get kj and convert to corresponding alphabetical integer number
            char kj = key[j % key_len];
            kj = toupper(kj);
            kj = (int) kj;
            kj -= 65;
            j++;

            // encipher pi with kj
            if (isupper(pi))
            {
                pi = (((int) pi - 65) + kj) % 26;
                pi += 65;
                pi = (char) pi;
            }

            else
            {
                pi = (((int) pi - 97) + kj) % 26;
                pi += 97;
                pi = (char) pi;
            }

            printf("%c", pi);
        }

    }

    printf("\n");
    return 0;
}


// Check whether a string contains only alphabetical characters
bool is_alpha(string x)
{
    for (int i = 0, n = strlen(x); i < n; i++)
    {
        if (!isalpha(x[i]))
        {
            return false;
        }
    }

    return true;
}