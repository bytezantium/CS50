// Headerfile for structs used in dictionary.c

// Maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45

// struct node
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;