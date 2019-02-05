// Implements a dictionary's functionality using a trie structure

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// Trie node structure
typedef struct t_node
{
    bool is_word;
    struct t_node *children[27];
}
t_node;

// Function to free trie node
void free_trie(t_node *x);

// Global t_node Root Node Pointer
t_node *root = NULL;

// Global Dictionary Load Flag
bool loaded = false;

// Global dictionary wordcount
unsigned long wordcount = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // temporary traversal pointer
    t_node *trav = root;

    // For each letter in input word
    char copy[strlen(word) + 1];
    strcpy(copy, word);
    for (int i = 0; i < strlen(copy); i++)
    {
        int index = 0;
        copy[i] = tolower(copy[i]); // Case insensitivity

        if (isalpha(copy[i])) // Convert letter to alphabetical index
        {
            index = (int) copy[i] - 97;
        }
        else
        {
            index = 26;
        }

        // Go to corresponding element in children
        if (!trav->children[index]) // if NULL
        {
            return false; // word is misspelled
        }

        trav = trav->children[index]; // if not NULL, move to next letter
    }
    // Once at the end of input word
    if (trav->is_word)
    {
        return true; // checks if is_word is true
    }

    return false;

}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open dictionary for reading
    FILE *dptr = fopen(dictionary, "r");
    if (!dptr)
    {
        fprintf(stderr, "Could not open %s.\n", dictionary);
        return false;
    }

    // Malloc space for root node
    root = malloc(sizeof(t_node));
    if (!root) // error checking
    {
        fprintf(stderr, "Error while loading dictionary into memory\n");
        fclose(dptr);
        return false;
    }
    // t_node root is_word false
    root->is_word = false;

    // t_node root children initialized to NULL
    for (int i = 0; i < 27; i++)
    {
        root->children[i] = NULL;
    }

    // Store words in string
    char word[LENGTH + 1];

    // Scan through every dictionary word
    while (fscanf(dptr, "%s", word) != EOF)
    {
        // temporary traversal pointer
        t_node *trav = root;

        // Iterate through t_node for each letter
        for (int i = 0; i < strlen(word); i++)
        {
            int index = 0;

            // Convert letter to alphabetical index
            if (isalpha(word[i]))
            {
                index = (int) word[i] - 97;
            }
            else
            {
                index = 26;
            }

            if (!trav->children[index]) // if NULL
            {
                t_node *new_t_node = malloc(sizeof(t_node)); // malloc a new node
                if (!new_t_node) // error checking
                {
                    fprintf(stderr, "Error while loading dictionary into memory\n");
                    fclose(dptr);
                    unload();
                    wordcount = 0;
                    return false;
                }
                new_t_node->is_word = false; // Initialize is_word member to false
                for (int j = 0; j < 27; j++)
                {
                    new_t_node->children[j] = NULL; // Initialize new node children to NULL
                }

                trav->children[index] = new_t_node; // Have children[index] point to new node.
            }

            trav = trav->children[index]; // move to next node

        } // for end

        trav->is_word = true; // end of word, is_word to true

        wordcount++; // increment global dictionary wordcount

        trav = root; // reset traversal pointer

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
    free_trie(root);

    return true;
}

// Frees complete trie from bottom to top
void free_trie(t_node *x)
{
    if (!x) // base case: stop when root itself has been freed
    {
        return;
    }

    for (int i = 0; i < 27; i++) // recursive case
    {
        free_trie(x->children[i]); // move all pointers to leaves
    }

    free(x); // free leaves
}