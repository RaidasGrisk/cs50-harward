/* CS50:          https://cs50.harvard.edu/weeks
*  Problem set 5: https://docs.cs50.net/2017/x/psets/5/pset5.html
*  Problem 1:     https://docs.cs50.net/problems/speller/speller.html
*
* The program loads a dictionary (as a structure of hash table with linked lists) and checks for misspelled words in a given text.
* The program also counts the number of words in text, and frees the memory used to load dictionary when its done spellcheking.
*/


#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdbool.h>
#include "dictionary.h"

// initiate variables
bool loaded = false;
int word_count = 0;
const int hashtable_size = 25000;

// define node (to build linked list)
typedef struct node
{
    char word[LENGTH+1];
    struct node *next;
}
node;

// define hash function
int hash(const char *word)
{
    // some examples of hash functions:

    // https://study.cs50.net/hashtables
    // int hash_id = toupper(word[0]) - 'A';

    // https://stackoverflow.com/questions/14409466/simple-hash-functions
    // unsigned int hash_id = 0;
    // unsigned int len = strlen(word);
    // for(int i = 0; i < len; i++)
    //     hash_id = word[i] + (hash_id << 6) + (hash_id << 16) - hash_id;

    // https://www.reddit.com/r/cs50/comments/1x6vc8/pset6_trie_vs_hashtable/cf9nlkn/
    // this one seems to be the fastest
    unsigned int hash_id = 0;
    unsigned int len = strlen(word);
    for (int i = 0; i < len; i++)
        hash_id = (hash_id << 2) ^ word[i];

    return hash_id % hashtable_size;
}

// initiate hashtable
node *hashtable[hashtable_size];


/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // cast letters to lower case
    int len = strlen(word);
    char *word_cpy = malloc(len+1);
    for (int i = 0; i < len; i++)
    {
        word_cpy[i] = tolower(word[i]);
    }
    word_cpy[len] = '\0';

    // get hashtable id
    node *cursor = hashtable[hash(word_cpy)];

    // check if word exist
    while (cursor != NULL)
    {
        if (strcasecmp(word_cpy, cursor->word) == 0)
        {
            free(word_cpy);
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }

    // fail
    free(word_cpy);
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{

    // placeholder for word
    char word[LENGTH+1];

    // clear the hastable
    for (int i = 0; i <= hashtable_size; i++)
        {
            hashtable[i] = NULL;
        }

    // open dictionary
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("Can not open dictionary!");
        return false;
    }

    // scan each word in a dictionary
    while (fscanf(dict, "%s", word) != EOF)
    {

        // malloc a new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            printf("Can not create new node!");
            return false;
        }

        // insert word into node
        // fscanf(dict, "%s", word); this is done in while declaration at the top
        strcpy(new_node->word, word);

        // get hash key
        int hash_id = hash(new_node->word);

        // make new hash entry if it does not exist, and work out pointers
        if (hashtable[hash_id] == NULL)
        {
            hashtable[hash_id] = new_node;
            new_node->next = NULL;
        }

        // if it exist, add new and work out pointers
        else
        {
            new_node->next = hashtable[hash_id];
            hashtable[hash_id] = new_node;
        }

        word_count++;
    }

    // close and success
    loaded = true;
    fclose(dict);
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    if (loaded)
    {
        return word_count;
    }
    else
    {
        return 0;
    }
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    for (int i = 0; i <= hashtable_size; i++)
    {
        node* cursor = hashtable[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor -> next;
            free(temp);
        }
    }

    // success
    loaded = false;
    return true;
}
