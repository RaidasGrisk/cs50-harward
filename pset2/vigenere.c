/* CS50:          https://cs50.harvard.edu/weeks
*  Problem set 2: https://docs.cs50.net/2017/x/psets/2/pset2.html
*  Problem 3:     https://docs.cs50.net/problems/vigenere/vigenere.html
*
* The code asks user to provide key-word and plaintext. Returns Vigenere ciphered text (https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)
*/

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[]){

    // check if used provided a single argument
    if (argc == 1 || argc > 2){
        printf("Error: something is wrong with number of arguments. Enter a single alphabetic key-word.");
        return 1;
    }

    // check if given argument is alphabet only
    for (int i = 0; i < strlen(argv[1]); i++){
        if (!isalpha(argv[1][i])){
            printf("Error: something is wrong with alphabetic letters. Enter a single alphabetic key-word.");
            return 1;
            break;
        }
    }

    // prompt for string
    string plaintext = get_string("plaintext:  ");

    // initiate other variables
    string key_word = argv[1];
    int key_len = strlen(key_word);
    int str_len = strlen(plaintext);
    int ciphered_char_id;
    int key[str_len];

    // convert word-key to array of ints
    for (int i = 0; i < key_len; i++){
        key[i] = tolower(key_word[i]) - 97;
    }

    // print ciphertext
    printf("ciphertext: ");

    // loop through each letter and cipher
    for (int c = 0; c < str_len; c++){

        // get ciphered_char_id if lower (97 - 122)
        if (islower(plaintext[c])){
            ciphered_char_id = ((plaintext[c] - 97 + key[c % key_len]) % 26) + 97;
        }

        // get ciphered_char_id if upper (65 - 90)
        if (isupper(plaintext[c])){
            ciphered_char_id = ((plaintext[c] - 65 + key[c % key_len]) % 26) + 65;
        }

        // get ciphered_char_id if not an alphabet letter (do not cipher)
        if (isalpha(plaintext[c]) == 0){
            ciphered_char_id = plaintext[c];
        }

        // insert ciphered char into ciphertext
        printf("%c", ciphered_char_id);

    }

    // return
    printf("\n");
    return 0;

}
