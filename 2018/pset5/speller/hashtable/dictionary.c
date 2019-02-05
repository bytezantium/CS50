// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"
#include "node.h"

// Hash Function found on Internet with one modification made (see bottom of file)
// Citation: http://www.cs.yale.edu/homes/aspnes/pinewiki/C(2f)HashTables.html?highlight=%28CategoryAlgorithmNotes%29
unsigned long hash(const char *s);

// Global Hash Table
node *hashtable[HASHTABLE_SIZE];

// Global Dictionary Load Flag
bool loaded = false;

// Global dictionary wordcount
unsigned long wordcount = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // convert words to lower case to get relevant hash
    char copy[strlen(word) + 1];
    strcpy(copy, word);
    for (int i = 0; i < strlen(copy); i++)
    {
        copy[i] = tolower(copy[i]);
    }

    if (hashtable[hash(copy)])
    {
        for (node *tmp = hashtable[hash(copy)]; tmp != NULL; tmp = tmp->next)
        {
            if (strcasecmp(copy, tmp->word) == 0)
            {
                return true;
            }
        }
    }

    return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open dictionary for reading
    FILE *dptr = fopen(dictionary, "r");
    if (dptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", dictionary);
        return false;
    }

    // Store words in string
    char word[LENGTH + 1];

    // Initialize Hashtable pointer array to NULL and store in global variable
    for (int i = 0; i < HASHTABLE_SIZE; i++)
    {
        hashtable[i] = NULL;
    }

    // Iterate over each word in the dictionary
    while (fscanf(dptr, "%s", word) != EOF)
    {
        // Allocate memory space for dictionary node
        node *new_node = malloc(sizeof(node));
        if (!new_node)
        {
            fprintf(stderr, "Error while loading dictionary into memory\n");
            fclose(dptr);
            unload();
            wordcount = 0;
            return false;
        }

        // Initialize new_node
        strcpy(new_node->word, word);
        new_node->next = NULL;

        wordcount++;

        // Store word in constant variable for hash function
        const char *s = (const char *) word;

        // Insert node into hash table
        if (!hashtable[hash(s)])
        {
            hashtable[hash(s)] = new_node;
        }
        // Insert node into linked list at hashcode index
        else
        {
            new_node->next = hashtable[hash(s)];
            hashtable[hash(s)] = new_node;
        }
    }

    // Check whether there was an error
    if (ferror(dptr))
    {
        fclose(dptr);
        fprintf(stderr, "Error reading %s.\n", dictionary);
        unload();
        wordcount = 0;
        return false;
    }

    // Close Dictionary
    fclose(dptr);

    // Success
    loaded = true;

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (loaded)
    {
        return wordcount;
    }

    return 0;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < HASHTABLE_SIZE; i++)
    {
        node *cursor = hashtable[i];

        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }

    // Success
    return true;
}

// Hash function (citation see top of file)
unsigned long hash(const char *s)
{
    unsigned long h;
    unsigned const char *us;

    /* cast s to unsigned const char * */
    /* this ensures that elements of s will be treated as having values >= 0 */
    us = (unsigned const char *) s;

    h = 0;
    while (*us != '\0')
    {
        h = h * MULTIPLIER + *us;
        us++;
    }

    // Modification for hashtable size
    h %= HASHTABLE_SIZE;

    return h;
}
