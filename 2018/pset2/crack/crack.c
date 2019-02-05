// CS50x 2018 Pset 2/crack

// Include crypt() function
#define _XOPEN_SOURCE
#include <unistd.h>

#include <stdio.h>
#include <string.h>

#include "node.h"

// Constants
#define MAX_LENGTH 5
#define MIN_LENGTH 2
#define LETTERS_LENGTH 58
#define HASHTABLE_SIZE 58



// Helper functions
bool pw_check(const char *password, const char *salt, const char *pw_hash);
// Global Hash Table
node *hashtable[HASHTABLE_SIZE];


int main(int argc, char *argv[])
{
    // Ensure user inputs exactly 1 command line argument of length 13
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./crack hash\n");
        return 1;
    }

    // declare variables for pw cracking
    const char *user_hash = argv[1];
    const char salt[3];

    for (int i = 0; i < 3; i++) // Extract first two characters from hash
    {
        if (i == 2)
        {
            salt[i] = '\0'
        }
        else
        {
            salt[i] = user_pw[i]
        }
    }

    const char letters[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    int length = MIN_LENGTH;

    char *password = pw_reveal(MAX_LENGTH, LETTERS_LENGTH, length, letters, pw_hash, salt);

    printf("%s\n", password);

    // Success
    return 0;

}

// Custom function to recursively generate alphabetical password permutations
char *pw_reveal(int MAX_LENGTH, int LETTERS_LENGTH, int length, const char *letters, const char *pw_hash, const char *salt)
{
    // Declare char array to store password tests
    const char password[length];
    password[length] = '\0';

    while (length <= MAX_LENGTH)
    {
        for (int index = 0; index < length; index++)
        {
            for (int letters_index = 0; letters_index < LETTERS_LENGTH; letters_index++)
            {
                password[index] = letters[letters_index];
                break;

            }

            if (pw_check(password, salt, pw_hash)) // base case
            {
                return password;
            }

        }

    }



        if (pw_check(password, salt, pw_hash)) // base case
        {
            return password;
        }

        lower_case++;

        else
        {
            password[length - length + index] = char (upper_case);
        }

        if (pw_check(password, salt, pw_hash)) // base case
        {
            return password;
        }

        upper_case++;
    }

    return pw_reveal(int MAX_LENGTH, int length + 1, int lower_case, int upper_case, const char *pw_hash, const char *salt)
}

bool pw_check(const char *password, const char *salt, const char *pw_hash)
{
    // crypt function: char *crypt(const char *key, const char *salt);
    if (!strcmp(crypt(password, salt), pw_hash)) // password hashes match
    {
        return true;
    }

    else
    {
        return false;
    }
}