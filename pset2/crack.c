/* CS50:          https://cs50.harvard.edu/weeks
*  Problem set 2: https://docs.cs50.net/2017/x/psets/2/pset2.html
*  Problem 4:     https://docs.cs50.net/problems/crack/crack.html
*
* The code cracks ten passwords using their hashes (cyphertext) using brute force. And prints out the result.
* This task is not implemented strictly as formulated on cs50 problem set.
*/

#define _GNU_SOURCE
#include <crypt.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <cs50.h>

int main(int argc, string argv[]){

    // check if user provided a valid argument
    if (argc != 2)
    {
        printf("Error: something is wrong with number of arguments.");
        return 1;
    }
    else
    {
        printf("Please wait. The password will be printed out as soon as the program cracks it.\n");
    }

    // initiate variables
    char dictionary[64] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ";
    char plaintext[5];
    char salt[3];
    string hash = argv[1];
    strncpy(salt, hash, 2);

    // generate a guess
    for (int i1 = 0; i1 < strlen(dictionary); i1++)
    {
        plaintext[0] = dictionary[i1];
        for (int i2 = 0; i2 < strlen(dictionary); i2++)
        {
            plaintext[1] = dictionary[i2];
            for (int i3 = 0; i3 < strlen(dictionary); i3++)
            {
                plaintext[2] = dictionary[i3];
                for (int i4 = 0; i4 < strlen(dictionary); i4++)
                {
                    plaintext[3] = dictionary[i4];

                    // a trick to generate guesses with length less than 4: '/0' instead of ' '
                    for (int c = 0; c < strlen(plaintext); c++)
                    {
                        if (plaintext[c] == ' ')
                        {
                            plaintext[c] = 0;
                        }
                    }

                    // encrypt generated guess and get its hash
                    char* crypt_hash = crypt(plaintext, salt);

                    // check if guess is correct
                    if (strcmp(crypt_hash, hash) == 0)
                    {
                        printf("Hash: %s, Pass: %s\n", hash, plaintext);
                        return 0;
                    }
                }
            }
        }
    }
}

