/* CS50:          https://cs50.harvard.edu/weeks
*  Problem set 2: https://docs.cs50.net/2017/x/psets/2/pset2.html
*  Problem 4:     https://docs.cs50.net/problems/crack/crack.html
*
* The code cracks ten passwords using their hashes (cyphertext) using brute force. And prints it out.
* This task is not implemented strictly as formulated on cs50 problem set. Cracking is the fun part.
* This thread helped me big time: https://www.reddit.com/r/cs50/comments/5rkl6z/what_the_crack/
*/

#define _GNU_SOURCE
#include <crypt.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void){

    // init dictionary of possible chracaters and known hashes table
    char dictionary[64] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ";
    const char* hash[10];
    hash[0] = "50.jPgLzVirkc";
    hash[1] = "50YHuxoCN9Jkc";
    hash[2] = "50QvlJWn2qJGE";
    hash[3] = "50CPlMDLT06yY";
    hash[4] = "50WUNAFdX/yjA";
    hash[5] = "50fkUxYHbnXGw";
    hash[6] = "50C6B0oz0HWzo";
    hash[7] = "50nq4RV/NVU0I";
    hash[8] = "50vtwu4ujL.Dk";
    hash[9] = "50i2t3sOSAZtk";

    // init empty array to store cracked passwords
    char passwords[10][5];

    // initiate empty string with 4 chars to store guess
    char plaintext[5];
    char plaintext_ready[5];

    // int book keeping vars
    int iteration = 0;
    int set_size = pow(strlen(dictionary), 4);

    // generate a guess
    for (int i1 = 0; i1 < strlen(dictionary); i1++){
        plaintext[0] = dictionary[i1];
        for (int i2 = 0; i2 < strlen(dictionary); i2++){
            plaintext[1] = dictionary[i2];
            for (int i3 = 0; i3 < strlen(dictionary); i3++){
                plaintext[2] = dictionary[i3];
                for (int i4 = 0; i4 < strlen(dictionary); i4++){
                    plaintext[3] = dictionary[i4];

                    // remove empty space to generate plaintext with length less than 4
                    // could not come up with a better solution to generate guesses with length less than 4
                    strcpy(plaintext_ready, plaintext);
                    for (int c = 0; c < strlen(plaintext_ready); c++){
                        if (plaintext[c] == ' '){
                            plaintext_ready[c] = 0;
                        }
                    }

                    // crypt generated guess and get hash
                    char* crypt_hash = crypt(plaintext_ready, "50");

                    // check if hash == crypt_hash and save it if guess is correct
                    for (int hash_id = 0; hash_id < 10; hash_id++){

                        if (strcmp(crypt_hash, hash[hash_id]) == 0){
                            strcpy(passwords[hash_id], plaintext_ready);
                        }
                    }

                    // book-keeping
                    if (iteration % 100000 == 0){
                        printf("progress: %f\n", (float)iteration / (float)set_size);
                    }
                    iteration = iteration + 1;
                }
            }
        }
    }

    printf("\nDone. Here are the cracked passwords:\n");
    for (int i = 0; i < 10; i++){
        printf("Hash: %s, pass: %s\n", hash[i], passwords[i]);
    }

}

